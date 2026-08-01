"""
Data Merger Module for Olist E-commerce Dataset.
Hợp nhất dữ liệu đa tầng từ Order Items, Payments, Reviews về Order Level và Customer Level.
"""

from pathlib import Path
import pandas as pd
import numpy as np

from src.data_loader import load_all_datasets, BASE_DIR

def build_master_orders_dataframe(datasets: dict = None) -> pd.DataFrame:
    """
    Merges all Olist relational tables into a unified Order-Level DataFrame.
    """
    if datasets is None:
        datasets = load_all_datasets()
        
    print("\n[INFO] Starting Multi-Table Data Merging Workflow...")
    
    # 1. Translate product categories
    products = datasets['products'].copy()
    cat_trans = datasets['category_translation'].copy()
    products = products.merge(cat_trans, on='product_category_name', how='left')
    products['product_category_name_english'] = products['product_category_name_english'].fillna(
        products['product_category_name'].fillna('unknown')
    )
    
    # 2. Merge order_items with product details
    items = datasets['order_items'].copy()
    items = items.merge(
        products[['product_id', 'product_category_name_english']], 
        on='product_id', 
        how='left'
    )
    
    # 3. Aggregate Order Items to Order Level
    order_items_agg = items.groupby('order_id').agg(
        total_item_price=('price', 'sum'),
        total_freight_value=('freight_value', 'sum'),
        total_item_count=('order_item_id', 'count'),
        unique_sellers_count=('seller_id', 'nunique'),
        main_category=('product_category_name_english', lambda x: x.mode()[0] if not x.empty and len(x.mode()) > 0 else 'unknown')
    ).reset_index()
    
    # 4. Aggregate Order Payments to Order Level
    payments = datasets['order_payments'].copy()
    order_payments_agg = payments.groupby('order_id').agg(
        total_payment_value=('payment_value', 'sum'),
        max_installments=('payment_installments', 'max'),
        primary_payment_type=('payment_type', lambda x: x.mode()[0] if not x.empty and len(x.mode()) > 0 else 'not_defined')
    ).reset_index()
    
    # 5. Aggregate Order Reviews to Order Level
    reviews = datasets['order_reviews'].copy()
    order_reviews_agg = reviews.groupby('order_id').agg(
        review_score=('review_score', 'mean'),
        review_count=('review_id', 'count')
    ).reset_index()
    
    # 6. Merge into Master Orders Table
    orders = datasets['orders'].copy()
    customers = datasets['customers'].copy()
    
    orders_master = orders.merge(customers[['customer_id', 'customer_unique_id', 'customer_zip_code_prefix', 'customer_city', 'customer_state']], on='customer_id', how='inner')
    orders_master = orders_master.merge(order_items_agg, on='order_id', how='left')
    orders_master = orders_master.merge(order_payments_agg, on='order_id', how='left')
    orders_master = orders_master.merge(order_reviews_agg, on='order_id', how='left')
    
    # 7. Convert Timestamp Columns
    time_cols = [
        'order_purchase_timestamp', 'order_approved_at', 
        'order_delivered_carrier_date', 'order_delivered_customer_date', 
        'order_estimated_delivery_date'
    ]
    for col in time_cols:
        orders_master[col] = pd.to_datetime(orders_master[col])
        
    # 8. Derived Order-Level Features
    orders_master['delivery_delay_days'] = (
        orders_master['order_delivered_customer_date'] - orders_master['order_estimated_delivery_date']
    ).dt.total_seconds() / (24 * 3600)
    
    orders_master['actual_delivery_days'] = (
        orders_master['order_delivered_customer_date'] - orders_master['order_purchase_timestamp']
    ).dt.total_seconds() / (24 * 3600)
    
    # Fill missing payment values with item price + freight if payment value missing
    orders_master['total_payment_value'] = orders_master['total_payment_value'].fillna(
        orders_master['total_item_price'] + orders_master['total_freight_value']
    )
    
    print("=" * 60)
    print(f"[SUCCESS] Master Orders DataFrame Created!")
    print(f"  • Shape: {orders_master.shape[0]:,} rows x {orders_master.shape[1]} columns")
    print(f"  • Unique Customers (customer_unique_id): {orders_master['customer_unique_id'].nunique():,}")
    print("=" * 60)
    
    return orders_master

def save_master_dataframe(df: pd.DataFrame, relative_path: str = "data/processed/master_orders.csv") -> Path:
    """Saves DataFrame to processed directory."""
    output_path = BASE_DIR / relative_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Saved master dataset to: {output_path}")
    return output_path

if __name__ == "__main__":
    df_master = build_master_orders_dataframe()
    save_master_dataframe(df_master)
