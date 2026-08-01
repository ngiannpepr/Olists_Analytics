# 🛒 Olist E-commerce Customer Segmentation & Behavioral Analytics (Đề 3)

## 📌 Overview
This repository contains a Senior-grade Data Science & Machine Learning implementation for **Customer Segmentation** using the Brazilian Olist E-Commerce Dataset.

The project transitions e-commerce analytics from generic marketing ("one-size-fits-all") to data-driven **Personalized Marketing** and **Product Recommendation Systems**.

## 📁 Project Structure

```text
d:/MindX_3/Final_Test/
├── DATA_SET/                 # Raw Olist CSV files
├── data/
│   ├── raw/                  # Reference to raw datasets
│   └── processed/            # Merged & cleaned customer-level dataset
├── notebooks/                # Modular Jupyter Notebooks
│   ├── 01_business_understanding_and_data_merging.ipynb
│   ├── 02_eda_and_data_cleaning.ipynb
│   ├── 03_feature_engineering_rfm.ipynb
│   ├── 04_clustering_model_building.ipynb
│   └── 05_business_recommendations.ipynb
├── src/                      # Production Python scripts
│   ├── __init__.py
│   ├── data_loader.py
│   ├── data_merger.py
│   ├── feature_engineering.py
│   └── clustering_engine.py
├── reports/                  # Generated figures and final executive report
│   ├── figures/
│   └── olist_customer_segmentation_report.md
├── requirements.txt
├── .gitignore
└── README.md
```

## 🎯 Key Objectives & Deliverables
1. **RFM + Behavioral Feature Engineering**: Extracted Recency, Frequency, Monetary value alongside review satisfaction score, delivery delay, payment installments, and product category diversity.
2. **K-Means Clustering & Evaluation**: Feature scaling (RobustScaler), log transformations, optimal cluster determination ($K=4$) validated via Silhouette Score and Elbow Method.
3. **Actionable Business Strategy**: Tailored campaigns for Marketing (Ads Targeting) and product features for Dev (Recommendation Engines).

## 🚀 How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run data processing & clustering pipeline
python -m src.data_merger
python -m src.feature_engineering
python -m src.clustering_engine

# 3. Explore Jupyter Notebooks
jupyter notebook notebooks/01_business_understanding_and_data_merging.ipynb
```
