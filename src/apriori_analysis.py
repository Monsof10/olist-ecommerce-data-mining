import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def prepare_basket(basket_data):
    """
    Prepare data for Apriori by creating a transaction matrix.
    Rows: order_id, Cols: product_category_name
    """
    # Group by order_id and product category, counting occurrences
    basket = (basket_data.groupby(['order_id', 'product_category_name'])['order_item_id']
              .count().unstack().reset_index().fillna(0)
              .set_index('order_id'))
    
    # Convert to 1/0
    basket = basket.map(lambda x: 1 if x > 0 else 0)
    
    return basket

def run_apriori(basket, min_support=0.01):
    """
    Run Apriori algorithm to find frequent itemsets.
    """
    # Apriori requires a lot of memory, so we'll use a relatively high min_support 
    # depending on dataset size. We will use the mlxtend implementation.
    # Convert boolean or 1/0 to bool to avoid warnings
    basket = basket.astype(bool)
    
    frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)
    
    return frequent_itemsets

def generate_association_rules(frequent_itemsets, metric="lift", min_threshold=1.0):
    """
    Generate association rules from frequent itemsets.
    """
    if frequent_itemsets.empty:
        print("No frequent itemsets found. Try lowering min_support.")
        return pd.DataFrame()
        
    rules = association_rules(frequent_itemsets, metric=metric, min_threshold=min_threshold)
    return rules
