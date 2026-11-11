import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def plot_rfm_distributions(rfm_df, output_dir):
    """
    Plot distributions of R, F, M.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    sns.histplot(rfm_df['Recency'], bins=50, ax=axes[0], color='skyblue')
    axes[0].set_title('Recency Distribution')
    
    # Frequency often has a huge skew (mostly 1)
    sns.countplot(data=rfm_df[rfm_df['Frequency'] <= 10], x='Frequency', ax=axes[1], color='lightgreen')
    axes[1].set_title('Frequency Distribution (<=10)')
    
    sns.histplot(rfm_df['Monetary'], bins=50, ax=axes[2], color='salmon')
    axes[2].set_title('Monetary Distribution')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'rfm_distributions.png'))
    plt.close()

def plot_clusters_pca(pca_df, labels, output_dir):
    """
    Plot 2D PCA clusters.
    """
    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x='PC1', y='PC2',
        hue=labels,
        palette='viridis',
        data=pca_df,
        legend='full',
        alpha=0.2,
        s=10
    )
    plt.title('Customer Clusters in 2D PCA Space')
    plt.savefig(os.path.join(output_dir, 'pca_clusters.png'))
    plt.close()

def plot_top_products(basket_data, output_dir, top_n=20):
    """
    Plot top product categories.
    """
    plt.figure(figsize=(12, 8))
    top_products = basket_data['product_category_name'].value_counts().head(top_n)
    
    sns.barplot(y=top_products.index, x=top_products.values, palette='Blues_r')
    plt.title(f'Top {top_n} Product Categories')
    plt.xlabel('Number of Items Sold')
    plt.ylabel('Category')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'top_products.png'))
    plt.close()

def plot_association_rules(rules, output_dir):
    """
    Scatter plot of support vs confidence with lift as color.
    """
    if rules.empty:
        return
        
    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x='support', y='confidence',
        size='lift', hue='lift',
        data=rules,
        sizes=(20, 200),
        palette='coolwarm',
        alpha=0.8
    )
    plt.title('Association Rules: Support vs Confidence (Color/Size = Lift)')
    plt.savefig(os.path.join(output_dir, 'association_rules.png'))
    plt.close()

def plot_elbow_and_silhouette(inertias, silhouette_scores, output_dir):
    """
    Plot Elbow and Silhouette for cluster validation.
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Elbow Plot
    k_vals = list(inertias.keys())
    axes[0].plot(k_vals, list(inertias.values()), 'bo-')
    axes[0].set_xlabel('Number of Clusters (K)')
    axes[0].set_ylabel('Inertia (Sum of Squared Distances)')
    axes[0].set_title('Elbow Method For Optimal K')
    axes[0].set_xticks(k_vals)
    
    # Silhouette Plot
    axes[1].plot(k_vals, list(silhouette_scores.values()), 'go-')
    axes[1].set_xlabel('Number of Clusters (K)')
    axes[1].set_ylabel('Silhouette Score')
    axes[1].set_title('Silhouette Score For Optimal K')
    axes[1].set_xticks(k_vals)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cluster_validation.png'))
    plt.close()

def plot_churn_feature_importance(importances, features, output_dir):
    """
    Plot feature importances from Churn model.
    """
    plt.figure(figsize=(10, 6))
    indices = np.argsort(importances)
    plt.barh(range(len(indices)), importances[indices], color='b', align='center')
    plt.yticks(range(len(indices)), [features[i] for i in indices])
    plt.xlabel('Relative Importance')
    plt.title('Churn Prediction: Feature Importances')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'churn_feature_importance.png'))
    plt.close()

def plot_clv_distribution(clv_values, output_dir):
    """
    Plot distribution of Customer Lifetime Value.
    """
    plt.figure(figsize=(10, 6))
    # Filter extreme outliers for better visualization
    q95 = clv_values.quantile(0.95)
    filtered_clv = clv_values[clv_values <= q95]
    
    sns.histplot(filtered_clv, bins=50, color='purple', kde=True)
    plt.title('Predicted Customer Lifetime Value (Next 12 Months) - Bottom 95%')
    plt.xlabel('Expected Value ($)')
    plt.ylabel('Number of Customers')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'clv_distribution.png'))
    plt.close()

def plot_review_topics(topics_dict, output_dir):
    """
    Plot bar charts of top words for each failure topic.
    """
    num_topics = len(topics_dict)
    fig, axes = plt.subplots(1, num_topics, figsize=(5 * num_topics, 6), sharex=True)
    
    if num_topics == 1:
        axes = [axes]
        
    for i, (topic, words_weights) in enumerate(topics_dict.items()):
        words = [w for w, _ in words_weights]
        weights = [w for _, w in words_weights]
        
        axes[i].barh(words, weights, color='indianred')
        axes[i].set_title(f'Topic {i}: {topic}', fontsize=12)
        axes[i].invert_yaxis()
        
    plt.suptitle('Top Words by Failure Topic (Negative Reviews)', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(os.path.join(output_dir, 'review_topics.png'))
    plt.close()
