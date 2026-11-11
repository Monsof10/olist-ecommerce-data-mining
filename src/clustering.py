import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def normalize_rfm(rfm_df):
    """
    Normalize RFM features using StandardScaler.
    Applies log transformation to Monetary and Recency to handle skewness if necessary.
    """
    features = ['Recency', 'Frequency', 'Monetary']
    rfm_scaled = rfm_df.copy()
    
    # Log transformation for highly skewed features
    # Add a small constant to handle zero values
    for col in features:
        rfm_scaled[col] = np.log1p(rfm_scaled[col])
        
    scaler = StandardScaler()
    rfm_scaled[features] = scaler.fit_transform(rfm_scaled[features])
    
    return rfm_scaled[features], scaler

def apply_kmeans(scaled_data, rfm_df, k=4):
    """
    Apply KMeans clustering.
    """
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(scaled_data)
    
    rfm_df['Cluster'] = kmeans.labels_
    
    return rfm_df, kmeans

def get_cluster_validation_metrics(scaled_data, max_k=8, sample_size=10000):
    """
    Calculate inertia and silhouette scores for K=2 to max_k.
    Returns dictionaries of inertias and silhouette scores.
    """
    inertias = {}
    silhouette_scores = {}
    
    np.random.seed(42)
    if len(scaled_data) > sample_size:
        sample_indices = np.random.choice(len(scaled_data), size=sample_size, replace=False)
        sample_data = scaled_data.iloc[sample_indices] if isinstance(scaled_data, pd.DataFrame) else scaled_data[sample_indices]
    else:
        sample_data = scaled_data
        
    for k in range(2, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(sample_data)
        inertias[k] = kmeans.inertia_
        silhouette_scores[k] = silhouette_score(sample_data, kmeans.labels_)
        
    return inertias, silhouette_scores
