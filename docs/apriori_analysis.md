# Explanation of `src/apriori_analysis.py`

### What it does
This script looks at what customers have in their shopping carts to find rules like "If someone buys X, they will probably also buy Y."

### The Logic Behind It
This is called "Market Basket Analysis". Imagine looking at millions of grocery store receipts. The Apriori algorithm counts how many times items are bought together. 

First, it turns all the shopping orders into a giant grid of yes/no (Did they buy electronics? Yes. Did they buy toys? No). Then, it scans the grid over and over to find patterns. If it notices that people who buy game consoles very often buy controllers at the exact same time, it creates an "Association Rule". Businesses use this logic to recommend products to you (e.g., "Customers who bought this also bought...").
