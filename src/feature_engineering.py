"""
Feature Engineering Module for Olist Customer Segmentation.
Aggregates Order-Level data to Customer Unique ID level and constructs RFM + Extended Behavioral Features.
"""

from pathlib import Path
import pandas as pd
import numpy as np

from src.data_loader import BASE_DIR

def build_customer_features(df_orders: pd.DataFrame) -> pd.DataFrame:
    """
    Constructs RFM and behavioral metrics per customer_unique_id.
    """
    print("\n[INFO] Starting Customer-Level Feature Engineering...")
    
    # Filter for valid orders (e.g. status delivered or completed)
    valid_orders = df_orders[df_orders['order_status'] == 'delivered'].copy()
    if valid_orders.empty:
        valid_orders = df_orders.copy()
        
    # Snapshot date for Recency calculation
    max_date = valid_orders['order_purchase_timestamp'].max()
    snapshot_date = max_date + pd.Timedelta(days=1)
    print(f"  • Max dataset date: {max_date.strftime('%Y-%m-%d')}")
    print(f"  • Snapshot date for Recency: {snapshot_date.strftime('%Y-%m-%d')}")
    
    # Group by customer_unique_id
    customer_agg = valid_orders.groupby('customer_unique_id').agg(
        # RFM Metrics
        last_purchase_timestamp=('order_purchase_timestamp', 'max'),
        frequency=('order_id', 'nunique'),
        monetary=('total_payment_value', 'sum'),
        
        # Extended Behavioral Metrics
        avg_review_score=('review_score', 'mean'),
        avg_delivery_delay=('delivery_delay_days', 'mean'),
        avg_actual_delivery_days=('actual_delivery_days', 'mean'),
        avg_installments=('max_installments', 'mean'),
        total_items=('total_item_count', 'sum'),
        category_diversity=('main_category', 'nunique'),
        
        # Categorical Preferences
        customer_state=('customer_state', 'first'),
        preferred_payment=('primary_payment_type', lambda x: x.mode()[0] if not x.empty and len(x.mode()) > 0 else 'credit_card')
    ).reset_index()
    
    # Recency in days
    customer_agg['recency'] = (snapshot_date - customer_agg['last_purchase_timestamp']).dt.total_seconds() / (24 * 3600)
    customer_agg['recency'] = customer_agg['recency'].round(1)
    
    # Average Order Value (AOV)
    customer_agg['avg_order_value'] = (customer_agg['monetary'] / customer_agg['frequency']).round(2)
    
    # Fill missing values gracefully
    overall_median_review = valid_orders['review_score'].median()
    customer_agg['avg_review_score'] = customer_agg['avg_review_score'].fillna(overall_median_review)
    customer_agg['avg_delivery_delay'] = customer_agg['avg_delivery_delay'].fillna(0.0)
    customer_agg['avg_actual_delivery_days'] = customer_agg['avg_actual_delivery_days'].fillna(
        valid_orders['actual_delivery_days'].median()
    )
    customer_agg['avg_installments'] = customer_agg['avg_installments'].fillna(1.0)
    customer_agg['total_items'] = customer_agg['total_items'].fillna(1)
    
    # Select feature set for RFM & Advanced Analytics
    feature_cols = [
        'customer_unique_id', 'recency', 'frequency', 'monetary', 'avg_order_value',
        'avg_review_score', 'avg_delivery_delay', 'avg_actual_delivery_days',
        'avg_installments', 'total_items', 'category_diversity', 'customer_state', 'preferred_payment'
    ]
    
    customer_df = customer_agg[feature_cols].copy()
    
    print("=" * 60)
    print(f"[SUCCESS] Customer Feature DataFrame Built!")
    print(f"  • Total Customer Profiles: {customer_df.shape[0]:,} customers")
    print(f"  • Total Features: {customer_df.shape[1]} features")
    print("=" * 60)
    
    return customer_df

def save_customer_features(df: pd.DataFrame, relative_path: str = "data/processed/customer_features.csv") -> Path:
    """Saves aggregated customer features to disk."""
    output_path = BASE_DIR / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Saved customer features dataset to: {output_path}")
    return output_path

if __name__ == "__main__":
    master_path = BASE_DIR / "data/processed/master_orders.csv"
    if not master_path.exists():
        from src.data_merger import build_master_orders_dataframe, save_master_dataframe
        df_master = build_master_orders_dataframe()
        save_master_dataframe(df_master)
    else:
        df_master = pd.read_csv(master_path, parse_dates=['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date'])
        
    df_customers = build_customer_features(df_master)
    save_customer_features(df_customers)
