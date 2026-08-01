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

def robust_scale(X: np.ndarray) -> np.ndarray:
    """RobustScaler using Median and Interquartile Range (IQR)."""
    median = np.median(X, axis=0)
    q25 = np.percentile(X, 25, axis=0)
    q75 = np.percentile(X, 75, axis=0)
    iqr = q75 - q25
    iqr[iqr == 0] = 1.0
    return (X - median) / iqr

def prepare_clustering_features(df_customers: pd.DataFrame) -> tuple[pd.DataFrame, np.ndarray, list[str]]:
    """Selects numerical features, applies Log1p transformation, and scales features."""
    features_to_use = ['recency', 'frequency', 'monetary', 'avg_review_score', 'avg_delivery_delay', 'avg_installments']
    df_feat = df_customers[features_to_use].copy()
    
    # Log transformation for skewed cols
    df_transformed = df_feat.copy()
    skewed_cols = ['recency', 'frequency', 'monetary', 'avg_installments']
    for col in skewed_cols:
        min_val = df_transformed[col].min()
        if min_val < 0:
            df_transformed[col] = np.log1p(df_transformed[col] - min_val)
        else:
            df_transformed[col] = np.log1p(df_transformed[col])
            
    X_val = df_transformed.values
    X_scaled = robust_scale(X_val)
    return df_feat, X_scaled, features_to_use

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

def fit_kmeans_and_visualize(df_customers: pd.DataFrame, X_scaled: np.ndarray, optimal_k: int = 4, output_dir: Path = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fits final K-Means model, assigns cluster labels, performs PCA 2D visualization, and computes summary statistics."""
    if output_dir is None:
        output_dir = BASE_DIR / "reports/figures"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n[INFO] Fitting Final K-Means Model with K={optimal_k}...")
    cluster_labels, centroids, inertia = kmeans_numpy(X_scaled, optimal_k)
    
    df_clustered = df_customers.copy()
    df_clustered['cluster'] = cluster_labels
    df_clustered['cluster_name'] = df_clustered['cluster'].map(lambda c: f"Cluster_{c}")
    
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
    
    return df_clustered, cluster_summary

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
        
    df_feat, X_scaled, feat_cols = prepare_clustering_features(df_customers)
    eval_results = find_optimal_k(X_scaled, range(2, 7))
    
    output_dir = BASE_DIR / "reports/figures"
    plot_clustering_metrics(eval_results, output_dir)
    
    df_clustered, summary = fit_kmeans_and_visualize(df_customers, X_scaled, optimal_k=4, output_dir=output_dir)
    
    # Save clustered output
    clustered_save_path = BASE_DIR / "data/processed/customer_clusters.csv"
    df_clustered.to_csv(clustered_save_path, index=False)
    print(f"[SUCCESS] Saved clustered customer dataset to: {clustered_save_path}")
