# Explanation of `src/fpgrowth_analysis.py`

### What it does
Exactly like `apriori_analysis.py`, this file finds products that are frequently bought together. However, it uses a different, much faster mathematical engine called "FP-Growth".

### The Logic Behind It
The Apriori method is great, but it has to scan the entire database over and over again, which takes a very long time if you have millions of sales. 

FP-Growth (Frequent Pattern Growth) is a smarter algorithm. Instead of scanning everything repeatedly, it builds a "tree" structure in the computer's memory. By walking through the branches of this tree, it can find the exact same shopping patterns (e.g., "Phone + Phone Case") in a fraction of the time. This script is used as the primary way to find product recommendations in this project because it is highly efficient.
