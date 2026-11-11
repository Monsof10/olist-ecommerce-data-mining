# Explanation of `src/rfm.py`

### What it does
This file calculates a score for every customer based on three simple things: **R**ecency, **F**requency, and **M**onetary value (RFM).

### The Logic Behind It
If you own a business, you want to know who your best customers are. RFM is a famous way to figure this out:
- **Recency**: How recently did the customer buy something? (If they bought yesterday, they are more active than someone who bought 2 years ago).
- **Frequency**: How many times have they bought from you? (A customer who ordered 10 times is better than a one-time buyer).
- **Monetary**: How much total money have they spent? 

This script goes through every customer's history, calculates these three numbers for them, and creates a clean summary table. It also filters out extremely strange data (like someone spending a million dollars by mistake) so our analysis stays accurate.
