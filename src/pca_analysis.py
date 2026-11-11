import pandas as pd
from sklearn.decomposition import PCA

def apply_pca(scaled_data, n_components=2):
    """
    Apply PCA to reduce dimensions (e.g., from 3 to 2 for visualization).
    """
    pca = PCA(n_components=n_components, random_state=42)
    pca_result = pca.fit_transform(scaled_data)
    
    pca_df = pd.DataFrame(data=pca_result, columns=[f'PC{i+1}' for i in range(n_components)])
    
    return pca_df, pca
