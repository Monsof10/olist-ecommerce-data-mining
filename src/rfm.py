import pandas as pd
import numpy as np

def calculate_rfm(rfm_data):
    """
    Compute Recency, Frequency, Monetary values per customer.
    """
    # Use max purchase date + 1 day as the snapshot date for Recency
    snapshot_date = rfm_data['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
    
    # Group by customer_unique_id
    rfm = rfm_data.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda x: (snapshot_date - x.max()).days,
        'order_id': 'nunique',
        'payment_value': 'sum'
    }).reset_index()
    
    # Rename columns
    rfm.rename(columns={
        'order_purchase_timestamp': 'Recency',
        'order_id': 'Frequency',
        'payment_value': 'Monetary'
    }, inplace=True)
    
    # Filter out outliers (e.g., extremely high monetary value, keep 99th percentile)
    q99 = rfm['Monetary'].quantile(0.99)
    rfm = rfm[rfm['Monetary'] <= q99]
    
    return rfm
