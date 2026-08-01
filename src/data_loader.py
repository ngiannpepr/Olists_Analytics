"""
Data Loader Utility Module for Olist E-commerce Dataset.
Provides functions to load raw datasets using pathlib for cross-platform compatibility.
"""

import os
import sys
from pathlib import Path
import pandas as pd

# Determine project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

def get_data_dir() -> Path:
    """Returns the directory containing raw CSV datasets."""
    dataset_dir = BASE_DIR / "DATA_SET"
    if dataset_dir.exists():
        return dataset_dir
    raw_dir = BASE_DIR / "data" / "raw"
    if raw_dir.exists():
        return raw_dir
    raise FileNotFoundError("Could not locate raw dataset folder (neither 'DATA_SET' nor 'data/raw').")

def load_all_datasets(data_dir: Path = None) -> dict[str, pd.DataFrame]:
    """
    Loads all 9 Olist CSV files into a dictionary of pandas DataFrames.
    
    Returns:
        dict: Mapping from dataset key to DataFrame.
    """
    if data_dir is None:
        data_dir = get_data_dir()
        
    file_mapping = {
        'customers': 'olist_customers_dataset.csv',
        'geolocation': 'olist_geolocation_dataset.csv',
        'order_items': 'olist_order_items_dataset.csv',
        'order_payments': 'olist_order_payments_dataset.csv',
        'order_reviews': 'olist_order_reviews_dataset.csv',
        'orders': 'olist_orders_dataset.csv',
        'products': 'olist_products_dataset.csv',
        'sellers': 'olist_sellers_dataset.csv',
        'category_translation': 'product_category_name_translation.csv'
    }
    
    datasets = {}
    print("=" * 60)
    print("[INFO] Loading Olist E-commerce CSV datasets...")
    print("=" * 60)
    
    for key, file_name in file_mapping.items():
        file_path = data_dir / file_name
        if not file_path.exists():
            raise FileNotFoundError(f"Missing required file: {file_path}")
        df = pd.read_csv(file_path)
        datasets[key] = df
        print(f"  * [{key:<20}] {file_name:<40} -> {df.shape[0]:>10,} rows, {df.shape[1]:>2} cols")
        
    print("=" * 60)
    print("[SUCCESS] All datasets loaded successfully!")
    print("=" * 60)
    return datasets

if __name__ == "__main__":
    datasets = load_all_datasets()
