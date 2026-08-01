"""
Script to generate clean, professional Jupyter Notebooks for the Olist Customer Segmentation pipeline.
"""

from pathlib import Path
import nbformat as nbf

BASE_DIR = Path(__file__).resolve().parent.parent
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)

def build_notebook_01():
    nb = nbf.v4.new_notebook()
    
    # Phase 1 Markdown
    md_p1 = """# 🛒 01. BUSINESS UNDERSTANDING & DATA MERGING ENGINE
## Project: Olist E-commerce Customer Segmentation (Đề 3)

### 📌 1. Business Context & Problem Statement
**Olist** là nền tảng thương mại điện tử hàng đầu tại Brazil, kết nối trực tiếp hàng nghìn doanh nghiệp vừa và nhỏ (SMEs) với các sàn giao dịch (marketplaces) lớn. Olist vận hành toàn bộ luồng thông tin bán hàng, thông báo người bán thực hiện đơn, hỗ trợ đối tác hậu cần (logistics) và tự động gửi khảo sát mức độ hài lòng khách hàng (NPS/Customer Satisfaction) sau khi giao hàng.

Trong bối cảnh chi phí gia tăng (CAC - Customer Acquisition Cost), việc cá nhân hóa trải nghiệm và phân nhóm khách hàng (**Customer Segmentation**) là chiến lược then chốt giúp tối ưu hóa Giá trị vòng đời khách hàng (Customer Lifetime Value - CLV).

---

### 🎯 2. Business Objectives & Stakeholder Requirements
Dự án được thiết kế để phục vụ 2 phòng ban chiến lược:

1. **Marketing Team (Tối ưu hóa tiếp thị Ads & Campaign):**
   - Chuyển tiếp từ tiếp thị đại trà sang **Personalized Marketing**.
   - Định danh chân dung từng cụm khách hàng (VIP/High-Value, Potential, At-Risk, Hibernating) dựa trên hành vi mua hàng và độ hài lòng.
   - Tối ưu chi phí quảng cáo (ROAS) và nâng tỷ lệ giữ chân (Retention Rate).

2. **Product & Dev Team (Hệ thống Đề xuất - Recommendation System):**
   - Thấu hiểu hành vi lựa chọn sản phẩm, phương thức thanh toán và thời gian giao hàng của từng phân khúc.
   - Xây dựng đầu vào (Customer Attributes & Segment Labels) cho hệ thống gợi ý sản phẩm cá nhân hóa.

---

### 🔑 3. Key Performance Indicators (KPIs)
- **Machine Learning Metric:** Silhouette Score > 0.45, phân cụm cân bằng, ý nghĩa hình học rõ ràng.
- **Business Metric:** Định hình 3-5 nhóm khách hàng có khả năng thực thi kinh doanh cao (Actionable Segments).
"""
    
    # Phase 2 Code
    code_p2 = """# Imports & Environment Setup
import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Add project root to sys.path
BASE_DIR = Path(os.getcwd()).parent if 'notebooks' in os.getcwd() else Path(os.getcwd())
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from src.data_loader import load_all_datasets
from src.data_merger import build_master_orders_dataframe, save_master_dataframe

# 1. Load Raw Datasets
datasets = load_all_datasets()

# 2. Execute Multi-Table Data Merging Pipeline
orders_master = build_master_orders_dataframe(datasets)

# 3. Save Processed Master Dataset
save_master_dataframe(orders_master)

# Display sample data
orders_master.head(5)
"""

    md_integrity = """### 🔍 Data Integrity & Schema Check
Kiểm tra cấu trúc và mức độ khuyết thiếu dữ liệu sau khi merge:
"""
    
    code_integrity = """# Check missing values summary
missing_summary = orders_master.isnull().sum().to_frame('missing_count')
missing_summary['missing_ratio (%)'] = (missing_summary['missing_count'] / len(orders_master) * 100).round(2)
missing_summary[missing_summary['missing_count'] > 0]
"""

    nb.cells = [
        nbf.v4.new_markdown_cell(md_p1),
        nbf.v4.new_code_cell(code_p2),
        nbf.v4.new_markdown_cell(md_integrity),
        nbf.v4.new_code_cell(code_integrity)
    ]
    
    output_path = NOTEBOOKS_DIR / "01_business_understanding_and_data_merging.ipynb"
    with open(output_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"[SUCCESS] Created notebook: {output_path}")

def build_notebook_02():
    nb = nbf.v4.new_notebook()
    
    md_header = """# 📊 02. EXPLORATORY DATA ANALYSIS (EDA) & DATA CLEANING

### 📌 Objectives:
1. Phân tích phân bố trạng thái đơn hàng (Order Status).
2. Trực quan hóa xu hướng doanh thu và lượng đơn theo thời gian.
3. Phân tích cấu trúc thanh toán (Payment Types, Installments) và đánh giá của khách hàng (Review Scores).
4. Làm sạch dữ liệu và xử lý giá trị ngoại lệ (Outliers).
"""

    code_eda = """import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = Path(os.getcwd()).parent if 'notebooks' in os.getcwd() else Path(os.getcwd())
master_path = BASE_DIR / "data/processed/master_orders.csv"
orders_df = pd.read_csv(master_path, parse_dates=['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date'])

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Order Status Distribution
sns.countplot(data=orders_df, y='order_status', ax=axes[0, 0], palette='viridis')
axes[0, 0].set_title('Distribution of Order Status', fontsize=12, fontweight='bold')

# 2. Payment Type Distribution
sns.countplot(data=orders_df, x='primary_payment_type', ax=axes[0, 1], palette='Set2')
axes[0, 1].set_title('Primary Payment Types Used', fontsize=12, fontweight='bold')

# 3. Review Score Distribution
sns.countplot(data=orders_df, x='review_score', ax=axes[1, 0], palette='Blues_r')
axes[1, 0].set_title('Customer Satisfaction Review Scores', fontsize=12, fontweight='bold')

# 4. Total Payment Value Distribution (Log scale)
sns.histplot(orders_df['total_payment_value'], bins=50, kde=True, ax=axes[1, 1], color='teal', log_scale=True)
axes[1, 1].set_title('Total Payment Value Distribution (Log Scale)', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()
"""

    nb.cells = [
        nbf.v4.new_markdown_cell(md_header),
        nbf.v4.new_code_cell(code_eda)
    ]
    
    output_path = NOTEBOOKS_DIR / "02_eda_and_data_cleaning.ipynb"
    with open(output_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"[SUCCESS] Created notebook: {output_path}")

def build_notebook_03():
    nb = nbf.v4.new_notebook()
    
    md_header = """# 🛠️ 03. FEATURE ENGINEERING & RFM CONSTRUCTION

### 📌 Objectives:
1. Xây dựng tập đặc trưng RFM Classic: **Recency**, **Frequency**, **Monetary**.
2. Xây dựng tập đặc trưng mở rộng E-commerce: **Satisfaction (Review Score)**, **Delivery Delay**, **Payment Installments**, **Category Diversity**.
3. Tổng hợp dữ liệu về cấp độ `customer_unique_id`.
"""

    code_fe = """import os
import sys
from pathlib import Path
import pandas as pd

BASE_DIR = Path(os.getcwd()).parent if 'notebooks' in os.getcwd() else Path(os.getcwd())
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from src.feature_engineering import build_customer_features, save_customer_features

master_path = BASE_DIR / "data/processed/master_orders.csv"
orders_df = pd.read_csv(master_path, parse_dates=['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date'])

customer_features = build_customer_features(orders_df)
save_customer_features(customer_features)

customer_features.describe().round(2)
"""

    nb.cells = [
        nbf.v4.new_markdown_cell(md_header),
        nbf.v4.new_code_cell(code_fe)
    ]
    
    output_path = NOTEBOOKS_DIR / "03_feature_engineering_rfm.ipynb"
    with open(output_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"[SUCCESS] Created notebook: {output_path}")

def build_notebook_04():
    nb = nbf.v4.new_notebook()
    
    md_header = """# 🤖 04. K-MEANS CLUSTERING & MODEL BUILDING

### 📌 Objectives:
1. Chuẩn hóa đặc trưng (Log Transformation + Robust Scaling).
2. Đánh giá số cụm tối ưu $K$ bằng **Elbow Method (Inertia)** và **Silhouette Score**.
3. Huấn luyện mô hình K-Means và trực quan hóa phân cụm (PCA 2D Scatter Plot).
"""

    code_ml = """import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(os.getcwd()).parent if 'notebooks' in os.getcwd() else Path(os.getcwd())
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from src.clustering_engine import prepare_clustering_features, find_optimal_k, plot_clustering_metrics, fit_kmeans_and_visualize

cust_path = BASE_DIR / "data/processed/customer_features.csv"
customer_df = pd.read_csv(cust_path)

df_feat, X_scaled, feat_cols = prepare_clustering_features(customer_df)
eval_results = find_optimal_k(X_scaled, k_range=range(2, 8))

output_dir = BASE_DIR / "reports/figures"
plot_clustering_metrics(eval_results, output_dir)

df_clustered, summary = fit_kmeans_and_visualize(customer_df, X_scaled, optimal_k=4, output_dir=output_dir)
df_clustered.to_csv(BASE_DIR / "data/processed/customer_clusters.csv", index=False)

summary
"""

    nb.cells = [
        nbf.v4.new_markdown_cell(md_header),
        nbf.v4.new_code_cell(code_ml)
    ]
    
    output_path = NOTEBOOKS_DIR / "04_clustering_model_building.ipynb"
    with open(output_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"[SUCCESS] Created notebook: {output_path}")

def build_notebook_05():
    nb = nbf.v4.new_notebook()
    
    md_header = """# 💡 05. BUSINESS RECOMMENDATIONS & STRATEGIC INSIGHTS

### 📌 Objectives:
1. Xây dựng chân dung khách hàng chi tiết (Customer Personas) cho từng phân cụm.
2. Đề xuất chiến lược cụ thể cho **Marketing Team** (Ads Targeting & Promotional Campaigns).
3. Đề xuất tính năng tích hợp cho **Product & Dev Team** (Personalized Recommendation System).
"""

    code_recs = """import os
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

BASE_DIR = Path(os.getcwd()).parent if 'notebooks' in os.getcwd() else Path(os.getcwd())
cluster_path = BASE_DIR / "data/processed/customer_clusters.csv"
df_clusters = pd.read_csv(cluster_path)

# Cluster Summary Analysis
summary = df_clusters.groupby('cluster_name')[['recency', 'frequency', 'monetary', 'avg_order_value', 'avg_review_score']].mean().round(2)
print("=== CLUSTER PROFILES SUMMARY ===")
print(summary)
"""

    nb.cells = [
        nbf.v4.new_markdown_cell(md_header),
        nbf.v4.new_code_cell(code_recs)
    ]
    
    output_path = NOTEBOOKS_DIR / "05_business_recommendations.ipynb"
    with open(output_path, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"[SUCCESS] Created notebook: {output_path}")

if __name__ == "__main__":
    build_notebook_01()
    build_notebook_02()
    build_notebook_03()
    build_notebook_04()
    build_notebook_05()
