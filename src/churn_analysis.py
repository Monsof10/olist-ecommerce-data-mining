import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

def run_churn_analysis(analytics_data):
    """
    Train a Random Forest model to predict customer churn.
    Churn is defined as Recency > 180 days.
    """
    df = analytics_data.copy()
    
    # Target Variable: Churned (1) if Recency > 180 days, else (0)
    df['Churned'] = (df['Recency'] > 180).astype(int)
    
    # Features
    # Fill missing values if any
    df.fillna(0, inplace=True)
    
    features = ['Frequency', 'Monetary', 'avg_review_score', 'avg_delivery_delay', 'avg_payment_installments']
    
    # Ensure all features exist, otherwise skip them or set to 0
    for f in features:
        if f not in df.columns:
            df[f] = 0
            
    X = df[features]
    y = df['Churned']
    
    # If all customers are churned or not churned, we can't train
    if len(y.unique()) < 2:
        print("Cannot train churn model: all customers belong to the same class.")
        return None, None, features
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train Random Forest
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10, class_weight='balanced')
    rf_model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = rf_model.predict(X_test)
    y_prob = rf_model.predict_proba(X_test)[:, 1]
    
    auc = roc_auc_score(y_test, y_prob)
    print(f"\nChurn Model ROC-AUC Score: {auc:.3f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    importances = rf_model.feature_importances_
    
    return rf_model, importances, features
