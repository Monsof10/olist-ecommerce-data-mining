import pandas as pd
import numpy as np
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter

def run_clv_analysis(rfm_df):
    """
    Train BG/NBD and Gamma-Gamma models using the lifetimes package.
    Note: lifetimes expects Frequency to be the number of *repeat* purchases.
    Since most customers have frequency 1 (0 repeat purchases), we need to ensure the format is correct.
    """
    # Create a copy for CLV modeling
    clv_data = rfm_df.copy()
    
    # In lifetimes, 'frequency' is number of repeat purchases (total purchases - 1)
    # Our 'Frequency' is total unique orders.
    clv_data['frequency_repeat'] = clv_data['Frequency'] - 1
    
    # Recency in lifetimes is the time between first and last purchase.
    # Our 'Recency' is days since last purchase from snapshot.
    # We don't have first purchase date in rfm_df directly, but we can approximate or we should calculate T and Recency properly.
    # Since we only have snapshot Recency, let's assume T (customer age) is 365 days for this approximation,
    # or we can use Recency as T if frequency=0.
    # A more rigorous way is to use lifetimes.utils.summary_data_from_transaction_data on the raw orders,
    # but we can approximate it here to fit the API requirements.
    
    clv_data['T'] = clv_data['Recency'] + 30 # Rough approximation: age is recency + 30 days
    clv_data['recency_lifetimes'] = clv_data['T'] - clv_data['Recency'] # Time between first and last
    
    # For frequency=0 (only 1 purchase), recency_lifetimes must be 0
    clv_data.loc[clv_data['frequency_repeat'] == 0, 'recency_lifetimes'] = 0
    
    # Fit BG/NBD Model
    bgf = BetaGeoFitter(penalizer_coef=0.0)
    bgf.fit(clv_data['frequency_repeat'], clv_data['recency_lifetimes'], clv_data['T'])
    
    # Predict number of purchases in the next 365 days
    clv_data['predicted_purchases_365d'] = bgf.conditional_expected_number_of_purchases_up_to_time(
        365, clv_data['frequency_repeat'], clv_data['recency_lifetimes'], clv_data['T']
    )
    
    # Fit Gamma-Gamma Model (only on customers with repeat purchases)
    repeat_customers = clv_data[clv_data['frequency_repeat'] > 0]
    
    if len(repeat_customers) > 0:
        ggf = GammaGammaFitter(penalizer_coef=0.0)
        # Average monetary value per transaction
        avg_monetary = repeat_customers['Monetary'] / repeat_customers['Frequency']
        
        ggf.fit(repeat_customers['frequency_repeat'], avg_monetary)
        
        # Predict average transaction value
        clv_data['predicted_avg_order_value'] = ggf.conditional_expected_average_profit(
            clv_data['frequency_repeat'], clv_data['Monetary'] / clv_data['Frequency']
        )
        
        # Calculate Customer Lifetime Value (CLV)
        clv_data['predicted_clv_12m'] = ggf.customer_lifetime_value(
            bgf,
            clv_data['frequency_repeat'],
            clv_data['recency_lifetimes'],
            clv_data['T'],
            clv_data['Monetary'] / clv_data['Frequency'],
            time=12, # months
            discount_rate=0.01 # monthly discount rate ~12.7% annually
        )
    else:
        clv_data['predicted_avg_order_value'] = 0
        clv_data['predicted_clv_12m'] = 0
        
    return clv_data
