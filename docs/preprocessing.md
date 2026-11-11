# Explanation of `src/preprocessing.py`

### What it does
This file cleans up the raw data and combines different tables together so they are easier to analyze.

### The Logic Behind It
Raw data is often messy or scattered. Think of it like receiving puzzle pieces in different boxes. 
1. **Cleaning Dates**: It goes through the data and makes sure that anything that looks like a date is actually understood by the computer as a real date and time, not just random text.
2. **Merging Data**: It takes different tables (like "orders" and "customers") and connects them. For example, if we want to know what a customer bought, we have to match the customer's ID with the order's ID.
3. **Filtering**: It throws away data that might mess up the analysis, like dropping orders that were never delivered or ignoring items that don't have a product category.

By the end of this script, we have neat, connected datasets ready for the actual math and science.
