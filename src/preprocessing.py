import pandas as pd

def preprocess_orders(orders_df):
    """
    Preprocess orders dataset: convert dates, handle missing values.
    """
    df = orders_df.copy()
    date_cols = ['order_purchase_timestamp', 'order_approved_at', 
                 'order_delivered_carrier_date', 'order_delivered_customer_date', 
                 'order_estimated_delivery_date']
    
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
    return df

def create_rfm_dataset(orders_df, payments_df, customers_df):
    """
    Merge ONLY orders, payments, customers for RFM analysis.
    """
    # 1. Merge orders and customers
    rfm_data = pd.merge(orders_df, customers_df, on='customer_id', how='inner')
    
    # 2. Merge with payments
    # Group payments by order_id to avoid duplication
    payments_grouped = payments_df.groupby('order_id', as_index=False)['payment_value'].sum()
    rfm_data = pd.merge(rfm_data, payments_grouped, on='order_id', how='inner')
    
    # Filter only delivered orders for accurate RFM
    rfm_data = rfm_data[rfm_data['order_status'] == 'delivered'].copy()
    
    # Handle missing dates for calculation
    rfm_data = rfm_data.dropna(subset=['order_purchase_timestamp'])
    
    return rfm_data

def create_basket_dataset(order_items_df, products_df, translations_df=None):
    """
    Merge order_items and products for Apriori analysis.
    """
    # Merge order items with products
    basket_data = pd.merge(order_items_df, products_df, on='product_id', how='inner')
    
    if translations_df is not None and not translations_df.empty:
        # Merge translations and replace the category name with English name
        basket_data = pd.merge(basket_data, translations_df, on='product_category_name', how='left')
        basket_data['product_category_name'] = basket_data['product_category_name_english'].fillna(basket_data['product_category_name'])
        basket_data = basket_data.drop(columns=['product_category_name_english'])
        
    # Drop items with no product category
    basket_data = basket_data.dropna(subset=['product_category_name']).copy()
    
    return basket_data

def create_customer_analytics_dataset(orders_df, payments_df, customers_df, reviews_df):
    """
    Merge orders, payments, customers, and reviews for customer analytics (churn, CLV).
    """
    # Base RFM data
    base_data = create_rfm_dataset(orders_df, payments_df, customers_df)
    
    # Calculate delivery delay
    orders_df['delivery_delay'] = (orders_df['order_delivered_customer_date'] - orders_df['order_estimated_delivery_date']).dt.days
    # Group delays by customer
    delay_data = pd.merge(orders_df[['customer_id', 'delivery_delay']], customers_df[['customer_id', 'customer_unique_id']], on='customer_id')
    avg_delay = delay_data.groupby('customer_unique_id')['delivery_delay'].mean().reset_index()
    avg_delay.rename(columns={'delivery_delay': 'avg_delivery_delay'}, inplace=True)
    
    # Calculate average review score
    if reviews_df is not None and not reviews_df.empty:
        # Reviews are linked to order_id
        order_customer_map = pd.merge(orders_df[['order_id', 'customer_id']], customers_df[['customer_id', 'customer_unique_id']], on='customer_id')
        reviews_mapped = pd.merge(reviews_df[['order_id', 'review_score']], order_customer_map, on='order_id', how='inner')
        avg_reviews = reviews_mapped.groupby('customer_unique_id')['review_score'].mean().reset_index()
        avg_reviews.rename(columns={'review_score': 'avg_review_score'}, inplace=True)
    else:
        avg_reviews = pd.DataFrame(columns=['customer_unique_id', 'avg_review_score'])
        
    # Calculate average payment installments
    if payments_df is not None and not payments_df.empty:
        payment_mapped = pd.merge(payments_df[['order_id', 'payment_installments']], order_customer_map, on='order_id', how='inner')
        avg_installments = payment_mapped.groupby('customer_unique_id')['payment_installments'].mean().reset_index()
        avg_installments.rename(columns={'payment_installments': 'avg_payment_installments'}, inplace=True)
    else:
        avg_installments = pd.DataFrame(columns=['customer_unique_id', 'avg_payment_installments'])
        
    # We will merge these into the RFM output later in main.py, or we can just return these analytics data
    # Actually, returning the joined data per customer is best.
    # We need to compute RFM first to join
    from src.rfm import calculate_rfm
    rfm = calculate_rfm(base_data)
    
    analytics_df = pd.merge(rfm, avg_delay, on='customer_unique_id', how='left')
    analytics_df = pd.merge(analytics_df, avg_reviews, on='customer_unique_id', how='left')
    analytics_df = pd.merge(analytics_df, avg_installments, on='customer_unique_id', how='left')
    
    return analytics_df
