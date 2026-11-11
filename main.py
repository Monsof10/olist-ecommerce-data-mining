import os
import pandas as pd
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

from src.load_data import load_all_data
from src.preprocessing import (
    preprocess_orders, 
    create_rfm_dataset, 
    create_basket_dataset,
    create_customer_analytics_dataset
)
from src.rfm import calculate_rfm
from src.clv_analysis import run_clv_analysis
from src.churn_analysis import run_churn_analysis
from src.clustering import normalize_rfm, apply_kmeans, get_cluster_validation_metrics
from src.pca_analysis import apply_pca
from src.nlp_analysis import run_nlp_analysis
from src.fpgrowth_analysis import run_fpgrowth_analysis
from src.visualization import (
    plot_rfm_distributions, 
    plot_clusters_pca, 
    plot_top_products, 
    plot_association_rules,
    plot_elbow_and_silhouette,
    plot_churn_feature_importance,
    plot_clv_distribution,
    plot_review_topics
)

def main():
    print("=== Olist Data Mining Project ===")
    
    # Create outputs directories if they don't exist
    os.makedirs('outputs/plots', exist_ok=True)
    os.makedirs('outputs/models', exist_ok=True)
    
    # --- STEP 1: DATA LOADING ---
    print("\n--- Step 1: Loading Data ---")
    datasets = load_all_data(data_path="../")
    
    if not datasets:
        print("Error: No datasets loaded. Please ensure CSV files are in the correct directory.")
        return
        
    # --- STEP 2 & 3: TASK-SPECIFIC DATASETS & PREPROCESSING ---
    print("\n--- Step 2 & 3: Preprocessing & Creating Task Datasets ---")
    orders_df = preprocess_orders(datasets.get('orders', pd.DataFrame()))
    
    print("Creating RFM Dataset...")
    rfm_data = create_rfm_dataset(orders_df, datasets.get('payments', pd.DataFrame()), datasets.get('customers', pd.DataFrame()))
    
    print("Creating Basket Dataset for Apriori...")
    basket_data = create_basket_dataset(
        datasets.get('order_items', pd.DataFrame()), 
        datasets.get('products', pd.DataFrame()),
        datasets.get('translations', None)
    )
    
    print("Creating Customer Analytics Dataset...")
    analytics_data = create_customer_analytics_dataset(
        orders_df, 
        datasets.get('payments', pd.DataFrame()), 
        datasets.get('customers', pd.DataFrame()),
        datasets.get('reviews', pd.DataFrame())
    )
    
    # --- STEP 4: RFM + CLUSTERING ---
    print("\n--- Step 4: RFM Calculation & Clustering ---")
    print("Calculating RFM...")
    rfm_df = calculate_rfm(rfm_data)
    
    print("Normalizing RFM features...")
    scaled_rfm, scaler = normalize_rfm(rfm_df)
    
    print("Applying K-Means Clustering (K=4)...")
    rfm_df, kmeans_model = apply_kmeans(scaled_rfm, rfm_df, k=4)
    
    print("Justifying K=4 using Silhouette Score (on 10,000 samples to save time)...")
    inertias, sil_scores = get_cluster_validation_metrics(scaled_rfm, max_k=8, sample_size=10000)
    print(f"Silhouette Score for K=4: {sil_scores[4]:.3f} (positive score indicates good separation)")
    
    print("Generating Cluster Validation Plots...")
    plot_elbow_and_silhouette(inertias, sil_scores, 'outputs/plots')
    
    print("\n--- Cluster Interpretation & Revenue by Cluster ---")
    cluster_summary = rfm_df.groupby('Cluster').agg({
        'Recency': 'mean',
        'Frequency': 'mean',
        'Monetary': ['mean', 'sum', 'count']
    }).reset_index()
    
    cluster_summary.columns = ['Cluster', 'Avg_Recency', 'Avg_Frequency', 'Avg_Monetary', 'Total_Revenue', 'Customer_Count']
    
    total_revenue = cluster_summary['Total_Revenue'].sum()
    total_customers = rfm_df.shape[0]
    
    cluster_summary['Revenue_Share_%'] = (cluster_summary['Total_Revenue'] / total_revenue) * 100
    cluster_summary['Customer_Share_%'] = (cluster_summary['Customer_Count'] / total_customers) * 100
    
    # Robust segment naming based on absolute characteristics
    def name_segment(row):
        r = row['Avg_Recency']
        f = row['Avg_Frequency']
        m = row['Avg_Monetary']
        
        if f > 1.0:
            return 'Slipping Loyal Customers'
        elif r > 250 and m < 100:
            return 'Lost Low-Value Spenders'
        elif r > 250 and m >= 100:
            return 'At-Risk High-Spenders'
        else:
            return 'New/Fresh Customers'
            
    cluster_summary['Segment_Name'] = cluster_summary.apply(name_segment, axis=1)
    
    print(cluster_summary[['Cluster', 'Segment_Name', 'Avg_Recency', 'Avg_Frequency', 'Avg_Monetary', 'Customer_Share_%', 'Revenue_Share_%']].to_string(index=False))
    
    # Save cluster results
    rfm_df = pd.merge(rfm_df, cluster_summary[['Cluster', 'Segment_Name']], on='Cluster', how='left')
    rfm_df.to_csv('outputs/models/customer_segments.csv', index=False)
    cluster_summary.to_csv('outputs/models/cluster_summary.csv', index=False)
    
    # --- STEP 5: PCA ---
    print("\n--- Step 5: Dimensionality Reduction (PCA) ---")
    pca_df, pca_model = apply_pca(scaled_rfm, n_components=2)
    print(f"Explained Variance Ratio: {pca_model.explained_variance_ratio_}")
    
    # --- STEP 5b: Predictive ML (Churn & CLV) ---
    print("\n--- Step 5b: Predictive ML Models ---")
    print("Running Customer Lifetime Value (CLV) Forecasting...")
    clv_df = run_clv_analysis(analytics_data)
    if clv_df is not None:
        clv_df.to_csv('outputs/models/customer_clv_predictions.csv', index=False)
        plot_clv_distribution(clv_df['predicted_clv_12m'], 'outputs/plots')
        print("CLV model trained and predictions saved.")
        
    print("Running Customer Churn Prediction...")
    rf_model, importances, features = run_churn_analysis(analytics_data)
    if rf_model is not None:
        plot_churn_feature_importance(importances, features, 'outputs/plots')
    
    # --- STEP 6: NLP (Review Sentiment & Topics) ---
    print("\n--- Step 6: Review Sentiment & Topic Modeling (NLP) ---")
    topics_dict, sentiment_model = run_nlp_analysis(datasets.get('reviews', pd.DataFrame()))
    if topics_dict:
        plot_review_topics(topics_dict, 'outputs/plots')
        print("NLP Topic modeling completed. Plot saved.")
        
    # --- STEP 7: ASSOCIATION RULES (FP-GROWTH) ---
    print("\n--- Step 7: Market Basket Analysis (FP-Growth) ---")
    rules = run_fpgrowth_analysis(basket_data, min_support=0.0001, min_lift=1.0)
    
    if not rules.empty:
        print(f"Found {len(rules)} positive association rules using FP-Growth.")
        rules.to_csv('outputs/models/fp_growth_association_rules.csv', index=False)
        plot_association_rules(rules, 'outputs/plots')
    else:
        print("No strong positive association rules found.")
        
    # --- STEP 8: VISUALIZATION ---
    print("\n--- Step 8: Generating Additional Visualizations ---")
    plot_rfm_distributions(rfm_df, 'outputs/plots')
    plot_clusters_pca(pca_df, rfm_df['Cluster'], 'outputs/plots')
    plot_top_products(basket_data, 'outputs/plots', top_n=15)
    
    # --- STEP 8: OUTPUTS & INSIGHTS ---
    print("\n--- Step 8 & 9: Complete! ---")
    print("All outputs have been saved to the /outputs directory.")
    
    print("\nBUSINESS INSIGHTS & DATA-DRIVEN CONCLUSIONS:")
    
    # Retention metric
    single_purchase_pct = (rfm_df['Frequency'] == 1).mean() * 100
    print(f"1. Low Customer Retention: {single_purchase_pct:.1f}% of your customers have only made a single purchase.")
    print("   Action: A strong post-purchase retention campaign is critical. Focus on onboarding and first-month follow-ups.")
    
    # Cluster metric
    champions = cluster_summary[cluster_summary['Segment_Name'] == 'Champions']
    if not champions.empty:
        champ_rev = champions['Revenue_Share_%'].values[0]
        champ_cust = champions['Customer_Share_%'].values[0]
        print(f"2. High-Value Concentration: The 'Champions' segment makes up {champ_cust:.1f}% of customers but drives {champ_rev:.1f}% of total revenue.")
        print("   Action: Protect this segment at all costs with VIP support and exclusive early-access loyalty programs.")
    
    # Association metric
    if not rules.empty:
        top_rule = rules.sort_values('lift', ascending=False).iloc[0]
        antecedent = list(top_rule['antecedents'])[0]
        consequent = list(top_rule['consequents'])[0]
        print(f"3. Product Synergies: Customers buying '{antecedent}' have a significantly higher likelihood (Lift: {top_rule['lift']:.1f}x) to also buy '{consequent}'.")
        print("   Action: Create targeted bundle discounts pairing these categories on the product page and checkout.")
    else:
        print("3. Product Synergies: Very few strong cross-category associations exist due to the single-item cart nature.")

if __name__ == "__main__":
    main()
