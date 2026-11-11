import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import NMF

def run_nlp_analysis(reviews_df):
    """
    Train a Portuguese sentiment classifier and extract failure topics.
    """
    if reviews_df is None or reviews_df.empty:
        print("No review data provided for NLP.")
        return None, None
        
    df = reviews_df.copy()
    
    # Filter only reviews with text
    df = df.dropna(subset=['review_comment_message'])
    
    if len(df) == 0:
        return None, None
        
    # We define sentiment: 1-2 = Negative (0), 4-5 = Positive (1). Ignore 3.
    df = df[df['review_score'] != 3]
    df['sentiment'] = (df['review_score'] >= 4).astype(int)
    
    print(f"Training sentiment model on {len(df)} reviews...")
    
    vectorizer = TfidfVectorizer(max_features=1000, min_df=5, stop_words=None) # We don't have PT stop_words by default in sklearn, we'll rely on min_df/max_features
    X = vectorizer.fit_transform(df['review_comment_message'])
    y = df['sentiment']
    
    model = LogisticRegression(random_state=42, max_iter=200)
    model.fit(X, y)
    accuracy = model.score(X, y)
    print(f"Sentiment Classifier Accuracy: {accuracy:.3f}")
    
    # Topic modeling on negative reviews
    neg_df = df[df['sentiment'] == 0]
    
    if len(neg_df) > 0:
        print(f"Extracting topics from {len(neg_df)} negative reviews...")
        neg_X = vectorizer.transform(neg_df['review_comment_message'])
        
        num_topics = 4
        nmf = NMF(n_components=num_topics, random_state=42, max_iter=200)
        nmf.fit(neg_X)
        
        feature_names = vectorizer.get_feature_names_out()
        topics_dict = {}
        
        for topic_idx, topic in enumerate(nmf.components_):
            top_features_ind = topic.argsort()[:-10 - 1:-1]
            top_features = [(feature_names[i], topic[i]) for i in top_features_ind]
            topics_dict[f"Topic {topic_idx+1}"] = top_features
            
        return topics_dict, model
        
    return None, model
