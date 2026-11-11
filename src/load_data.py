import pandas as pd
import os

def load_all_data(data_path="../"):
    """
    Load all necessary Olist datasets.
    """
    datasets = {}
    
    files_to_load = {
        'orders': 'olist_orders_dataset.csv',
        'customers': 'olist_customers_dataset.csv',
        'order_items': 'olist_order_items_dataset.csv',
        'products': 'olist_products_dataset.csv',
        'payments': 'olist_order_payments_dataset.csv',
        'reviews': 'olist_order_reviews_dataset.csv',
        'translations': 'product_category_name_translation.csv'
    }
    
    for name, filename in files_to_load.items():
        filepath = os.path.join(data_path, filename)
        if os.path.exists(filepath):
            datasets[name] = pd.read_csv(filepath)
            print(f"Loaded {name} dataset: {datasets[name].shape}")
        else:
            print(f"Warning: {filepath} not found.")
            
    return datasets
