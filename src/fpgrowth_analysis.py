import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules

def run_fpgrowth_analysis(basket_data, min_support=0.0001, min_lift=1.0):
    """
    Prepare full basket and run FP-Growth to find association rules.
    """
    print("Preparing full basket for FP-Growth...")
    # Since FP-growth is efficient, we can use the entire dataset
    basket = (basket_data.groupby(['order_id', 'product_category_name'])['order_item_id']
              .count().unstack().reset_index().fillna(0)
              .set_index('order_id'))
    
    # Convert to boolean
    basket = basket.map(lambda x: True if x > 0 else False)
    
    print("Running FP-Growth...")
    frequent_itemsets = fpgrowth(basket, min_support=min_support, use_colnames=True)
    
    print("Generating Association Rules...")
    if frequent_itemsets.empty:
        print("No frequent itemsets found.")
        return pd.DataFrame()
        
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_lift)
    
    return rules
