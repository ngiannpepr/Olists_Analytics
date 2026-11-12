"""
Clustering Engine Module for Olist Customer Segmentation.
Handles Data Transformation, Feature Scaling, K-Means Clustering, Hyperparameter Evaluation, and Visualization.
Features fallback to pure NumPy/SciPy to guarantee execution across all Python environments.
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.data_loader import BASE_DIR

# Set plot style safely
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 300

def robust_scale(X: np.ndarray, medians: np.ndarray = None, iqrs: np.ndarray = None) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """RobustScaler using Median and Interquartile Range (IQR). Returns scaled matrix, medians, and iqrs."""
    if medians is None:
        medians = np.median(X, axis=0)
    if iqrs is None:
        q25 = np.percentile(X, 25, axis=0)
        q75 = np.percentile(X, 75, axis=0)
        iqrs = q75 - q25
        iqrs[iqrs == 0] = 1.0
    scaled = (X - medians) / iqrs
    return scaled, medians, iqrs

def prepare_clustering_features(df_customers: pd.DataFrame) -> tuple[pd.DataFrame, np.ndarray, list[str], np.ndarray, np.ndarray, dict]:
    """Selects numerical features, applies Log1p transformation with shift tracking, and scales features."""
    features_to_use = ['recency', 'frequency', 'monetary', 'avg_review_score', 'avg_delivery_delay', 'avg_installments']
    df_feat = df_customers[features_to_use].copy()
    
    # Log transformation for skewed cols with train shift tracking
    df_transformed = df_feat.copy()
    skewed_cols = ['recency', 'frequency', 'monetary', 'avg_installments']
    train_log_shifts = {}
    for col in skewed_cols:
        min_val = df_transformed[col].min()
        shift = float(min_val) if min_val < 0 else 0.0
        train_log_shifts[col] = shift
        df_transformed[col] = np.log1p(df_transformed[col] - shift)
            
    X_val = df_transformed.values
    X_scaled, train_medians, train_iqrs = robust_scale(X_val)
    return df_feat, X_scaled, features_to_use, train_medians, train_iqrs, train_log_shifts

def derive_dynamic_cluster_mapping(df_clustered: pd.DataFrame, features_to_use: list[str]) -> dict:
    """Dynamically computes feature means per cluster and assigns persona names based on rule hierarchy."""
    cluster_means = df_clustered.groupby('cluster')[features_to_use].mean()
    dynamic_map = {}
    unassigned = set(cluster_means.index)

    # 1. Max avg_delivery_delay -> Severe Delivery Delay & At-Risk
    delay_cluster = cluster_means.loc[list(unassigned), 'avg_delivery_delay'].idxmax()
    dynamic_map[delay_cluster] = 'Severe Delivery Delay & At-Risk'
    unassigned.remove(delay_cluster)

    # 2. Max monetary -> High-Value Installment Spenders
    high_val_cluster = cluster_means.loc[list(unassigned), 'monetary'].idxmax()
    dynamic_map[high_val_cluster] = 'High-Value Installment Spenders'
    unassigned.remove(high_val_cluster)

    # 3. Min avg_review_score -> Dissatisfied / Low CSAT Shoppers
    low_csat_cluster = cluster_means.loc[list(unassigned), 'avg_review_score'].idxmin()
    dynamic_map[low_csat_cluster] = 'Dissatisfied / Low CSAT Shoppers'
    unassigned.remove(low_csat_cluster)

    # 4. Remaining -> Core Budget Shoppers
    remaining = list(unassigned)[0]
    dynamic_map[remaining] = 'Core Budget Shoppers'

    return dynamic_map

def kmeans_numpy(X: np.ndarray, k: int, max_iter: int = 100, seed: int = 42) -> tuple[np.ndarray, np.ndarray, float]:
    """Pure NumPy K-Means implementation for robust execution."""
    np.random.seed(seed)
    n_samples, n_features = X.shape
    
    # Randomly initialize centroids
    random_indices = np.random.choice(n_samples, k, replace=False)
    centroids = X[random_indices].copy()
    
    labels = np.zeros(n_samples, dtype=int)
    for _ in range(max_iter):
        # Compute distances to all centroids (N x K)
        distances = np.linalg.norm(X[:, np.newaxis, :] - centroids[np.newaxis, :, :], axis=2)
        new_labels = np.argmin(distances, axis=1)
        
        if np.array_equal(labels, new_labels):
            break
        labels = new_labels
        
        # Update centroids
        for ci in range(k):
            mask = (labels == ci)
            if np.any(mask):
                centroids[ci] = X[mask].mean(axis=0)
                
    # Inertia / WCSS
    inertia = 0.0
    for ci in range(k):
        mask = (labels == ci)
        if np.any(mask):
            inertia += np.sum((X[mask] - centroids[ci]) ** 2)
            
    return labels, centroids, float(inertia)

def calculate_silhouette_score_sample(X: np.ndarray, labels: np.ndarray, sample_size: int = 5000, seed: int = 42) -> float:
    """Calculates approximate silhouette score on a random sample."""
    np.random.seed(seed)
    n_samples = X.shape[0]
    if n_samples > sample_size:
        idx = np.random.choice(n_samples, sample_size, replace=False)
        X_s = X[idx]
        labels_s = labels[idx]
    else:
        X_s = X
        labels_s = labels
        
    unique_labels = np.unique(labels_s)
    if len(unique_labels) < 2:
        return 0.0
        
    n_s = X_s.shape[0]
    sil_scores = []
    
    # Distance matrix
    dist_matrix = np.linalg.norm(X_s[:, np.newaxis, :] - X_s[np.newaxis, :, :], axis=2)
    
    for i in range(n_s):
        c_i = labels_s[i]
        same_cluster_mask = (labels_s == c_i)
        same_cluster_mask[i] = False
        
        if np.sum(same_cluster_mask) == 0:
            a_i = 0.0
        else:
            a_i = np.mean(dist_matrix[i, same_cluster_mask])
            
        b_i = np.inf
        for other_c in unique_labels:
            if other_c == c_i:
                continue
            other_cluster_mask = (labels_s == other_c)
            mean_dist_other = np.mean(dist_matrix[i, other_cluster_mask])
            if mean_dist_other < b_i:
                b_i = mean_dist_other
                
        s_i = (b_i - a_i) / max(a_i, b_i) if max(a_i, b_i) > 0 else 0.0
        sil_scores.append(s_i)
        
    return float(np.mean(sil_scores))

def pca_2d(X: np.ndarray) -> np.ndarray:
    """PCA 2D projection using SVD."""
    X_centered = X - np.mean(X, axis=0)
    U, S, Vt = np.linalg.svd(X_centered, full_matrices=False)
    return X_centered @ Vt[:2].T

def find_optimal_k(X_scaled: np.ndarray, k_range: range = range(2, 7)) -> dict:
    """Evaluates K-Means clustering metrics across K range."""
    results = {'k': [], 'inertia': [], 'silhouette': []}
    print("\n[INFO] Evaluating Optimal Number of Clusters (K)...")
    
    for k in k_range:
        labels, centroids, inertia = kmeans_numpy(X_scaled, k)
        sil = calculate_silhouette_score_sample(X_scaled, labels, sample_size=3000)
        
        results['k'].append(k)
        results['inertia'].append(inertia)
        results['silhouette'].append(sil)
        print(f"  * K = {k} | Inertia = {inertia:10.1f} | Silhouette Score = {sil:.4f}")
        
    return results

def plot_clustering_metrics(results: dict, output_dir: Path) -> Path:
    """Plots and saves Elbow and Silhouette Score curves."""
    output_dir.mkdir(parents=True, exist_ok=True)
    fig, ax1 = plt.subplots(figsize=(10, 5))

    color = 'tab:blue'
    ax1.set_xlabel('Number of Clusters (K)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Inertia / WCSS', color=color, fontsize=12, fontweight='bold')
    ax1.plot(results['k'], results['inertia'], marker='o', color=color, linewidth=2, label='Inertia')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True, linestyle='--', alpha=0.5)

    ax2 = ax1.twinx()  
    color = 'tab:red'
    ax2.set_ylabel('Silhouette Score', color=color, fontsize=12, fontweight='bold')
    ax2.plot(results['k'], results['silhouette'], marker='s', color=color, linewidth=2, linestyle='--', label='Silhouette Score')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Olist Customer Segmentation: K-Means Evaluation (Elbow & Silhouette)', fontsize=14, fontweight='bold', pad=15)
    fig.tight_layout()
    
    save_path = output_dir / "kmeans_evaluation_metrics.png"
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Saved evaluation plot to: {save_path}")
    return save_path

def fit_kmeans_and_visualize(df_customers: pd.DataFrame, X_scaled: np.ndarray, optimal_k: int = 4, output_dir: Path = None) -> tuple[pd.DataFrame, pd.DataFrame, np.ndarray, dict]:
    """Fits final K-Means model, assigns cluster labels dynamically, performs PCA 2D visualization, and computes summary statistics."""
    if output_dir is None:
        output_dir = BASE_DIR / "reports/figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[INFO] Fitting Final K-Means Model with K={optimal_k}...")
    cluster_labels, centroids, inertia = kmeans_numpy(X_scaled, optimal_k)
    
    df_clustered = df_customers.copy()
    df_clustered['cluster'] = cluster_labels
    
    # Compute dynamic persona mapping based on cluster feature profiles
    features_to_use = ['recency', 'frequency', 'monetary', 'avg_review_score', 'avg_delivery_delay', 'avg_installments']
    dynamic_map = derive_dynamic_cluster_mapping(df_clustered, features_to_use)
    df_clustered['cluster_name'] = df_clustered['cluster'].map(lambda c: f"Cluster_{c}: {dynamic_map[c]}")
    
    # Perform PCA 2D Projection
    X_pca = pca_2d(X_scaled)
    df_clustered['pca_1'] = X_pca[:, 0]
    df_clustered['pca_2'] = X_pca[:, 1]
    
    # Plot PCA Scatter Plot
    plt.figure(figsize=(10, 7))
    sns.scatterplot(
        data=df_clustered,
        x='pca_1', y='pca_2',
        hue='cluster_name',
        palette='Set2',
        alpha=0.7,
        s=40,
        edgecolor=None
    )
    plt.title(f'Olist Customer Segments Visualization (PCA 2D Projection, K={optimal_k})', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('PCA Component 1', fontsize=11)
    plt.ylabel('PCA Component 2', fontsize=11)
    plt.legend(title='Customer Segment', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    pca_save_path = output_dir / "cluster_pca_scatter.png"
    plt.savefig(pca_save_path, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Saved PCA cluster scatter plot to: {pca_save_path}")
    
    # Calculate Cluster Summary Profile
    profile_cols = ['recency', 'frequency', 'monetary', 'avg_order_value', 'avg_review_score', 'avg_delivery_delay', 'avg_installments']
    cluster_summary = df_clustered.groupby('cluster_name')[profile_cols].agg(['mean', 'median', 'count']).round(2)
    
    return df_clustered, cluster_summary, centroids, dynamic_map

def perform_anova_tests(df_clustered: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    """Performs one-way ANOVA hypothesis test across clusters for each feature."""
    from scipy import stats
    results = []
    clusters = df_clustered['cluster'].unique()
    
    for feat in features:
        groups = [df_clustered[df_clustered['cluster'] == c][feat].dropna().values for c in clusters]
        f_stat, p_val = stats.f_oneway(*groups)
        results.append({
            'feature': feat,
            'f_statistic': round(f_stat, 2),
            'p_value': p_val,
            'is_statistically_significant': p_val < 0.001
        })
        
    return pd.DataFrame(results)

def evaluate_cluster_stability(X_scaled: np.ndarray, optimal_k: int = 4, n_iterations: int = 5, sample_ratio: float = 0.8, seed: int = 42) -> dict:
    """Evaluates cluster stability using bootstrap subsampling and Adjusted Rand Index (ARI)."""
    from sklearn.metrics import adjusted_rand_score
    np.random.seed(seed)
    n_samples = X_scaled.shape[0]
    sample_size = int(n_samples * sample_ratio)
    
    # Baseline model on full dataset
    labels_full, centroids_full, _ = kmeans_numpy(X_scaled, optimal_k, seed=seed)
    
    ari_scores = []
    for i in range(n_iterations):
        idx = np.random.choice(n_samples, sample_size, replace=False)
        X_sub = X_scaled[idx]
        labels_sub, _, _ = kmeans_numpy(X_sub, optimal_k, seed=seed + i + 1)
        
        # Compare ground truth labels on sub-sample with full model labels on sub-sample
        ari = adjusted_rand_score(labels_full[idx], labels_sub)
        ari_scores.append(ari)
        
    mean_ari = float(np.mean(ari_scores))
    std_ari = float(np.std(ari_scores))
    print(f"[VALIDATION] Cluster Stability (Bootstrap ARI across {n_iterations} runs): {mean_ari:.4f} (+/- {std_ari:.4f})")
    return {'ari_scores': ari_scores, 'mean_ari': mean_ari, 'std_ari': std_ari}

def predict_new_customer_segment(df_new: pd.DataFrame, centroids: np.ndarray, feature_cols: list[str], train_medians: np.ndarray, train_iqrs: np.ndarray, train_log_shifts: dict = None, cluster_name_map: dict = None) -> pd.DataFrame:
    """Predicts cluster label and distance for new customer data using pre-fitted training medians, IQRs & log shifts."""
    df_pred = df_new[feature_cols].copy()
    if train_log_shifts is None:
        train_log_shifts = {}
        
    skewed_cols = ['recency', 'frequency', 'monetary', 'avg_installments']
    for col in skewed_cols:
        if col in df_pred.columns:
            shift = train_log_shifts.get(col, 0.0)
            df_pred[col] = np.log1p(df_pred[col] - shift)
                
    X_val = df_pred.values
    iqrs_safe = np.where(train_iqrs == 0, 1.0, train_iqrs)
    X_scaled = (X_val - train_medians) / iqrs_safe
    
    # Compute Euclidean distance to centroids
    distances = np.linalg.norm(X_scaled[:, np.newaxis, :] - centroids[np.newaxis, :, :], axis=2)
    assigned_cluster = np.argmin(distances, axis=1)
    min_distances = np.min(distances, axis=1)
    
    result_df = df_new.copy()
    result_df['predicted_cluster'] = assigned_cluster
    if cluster_name_map:
        result_df['predicted_cluster_name'] = [f"Cluster_{c}: {cluster_name_map.get(c, 'Unknown')}" for c in assigned_cluster]
    result_df['distance_to_centroid'] = np.round(min_distances, 4)
    return result_df

def plot_cluster_category_distribution(df_master: pd.DataFrame, df_clustered: pd.DataFrame, output_dir: Path = None) -> Path:
    """Plots and saves product category distribution per customer segment."""
    if output_dir is None:
        output_dir = BASE_DIR / "reports/figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    merged = df_master.merge(df_clustered[['customer_unique_id', 'cluster', 'cluster_name']], on='customer_unique_id', how='inner')
    
    # Get top 6 overall categories
    top_6_cats = merged['main_category'].value_counts().head(6).index.tolist()
    cat_df = merged[merged['main_category'].isin(top_6_cats)]

    plt.figure(figsize=(12, 6))
    chart = sns.countplot(
        data=cat_df,
        x='cluster_name',
        hue='main_category',
        palette='Set2'
    )
    plt.title('Olist Product Category Share by Customer Segment (Top 6 Categories)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Customer Segment', fontsize=12, fontweight='bold')
    plt.ylabel('Order Count', fontsize=12, fontweight='bold')
    plt.xticks(rotation=15, ha='right')
    plt.legend(title='Product Main Category', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()

    save_path = output_dir / "cluster_category_distribution.png"
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Saved category distribution plot to: {save_path}")
    return save_path

if __name__ == "__main__":
    cust_path = BASE_DIR / "data/processed/customer_features.csv"
    if not cust_path.exists():
        from src.feature_engineering import build_customer_features, save_customer_features
        from src.data_merger import build_master_orders_dataframe
        df_master = build_master_orders_dataframe()
        df_customers = build_customer_features(df_master)
        save_customer_features(df_customers)
    else:
        df_customers = pd.read_csv(cust_path)
        from src.data_merger import build_master_orders_dataframe
        master_path = BASE_DIR / "data/processed/master_orders.csv"
        df_master = pd.read_csv(master_path) if master_path.exists() else build_master_orders_dataframe()
        
    df_feat, X_scaled, feat_cols, train_medians, train_iqrs, train_log_shifts = prepare_clustering_features(df_customers)
    eval_results = find_optimal_k(X_scaled, range(2, 7))
    
    output_dir = BASE_DIR / "reports/figures"
    plot_clustering_metrics(eval_results, output_dir)
    
    df_clustered, summary, centroids, dynamic_map = fit_kmeans_and_visualize(df_customers, X_scaled, optimal_k=4, output_dir=output_dir)
    plot_cluster_category_distribution(df_master, df_clustered, output_dir)
    
    # Statistical ANOVA Validation
    anova_df = perform_anova_tests(df_clustered, feat_cols)
    print("\n[VALIDATION] One-Way ANOVA Statistical Hypothesis Testing Across Clusters:")
    print(anova_df.to_string(index=False))
    
    # Stability Test
    stability_res = evaluate_cluster_stability(X_scaled, optimal_k=4)
    
    # Save clustered output
    clustered_save_path = BASE_DIR / "data/processed/customer_clusters.csv"
    df_clustered.to_csv(clustered_save_path, index=False)
    print(f"[SUCCESS] Saved clustered customer dataset to: {clustered_save_path}")



