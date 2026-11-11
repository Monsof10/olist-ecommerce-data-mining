# Explanation of `src/load_data.py`

### What it does
This file is responsible for bringing all the raw data into the project so it can be analyzed. 

### The Logic Behind It
Imagine you have a bunch of Excel spreadsheets saved on your computer (like lists of customers, orders, products, and reviews). Before you can analyze them, you need to open them all up. 

This script looks for specific files (like `olist_orders_dataset.csv` and `olist_customers_dataset.csv`), reads them, and loads them into the computer's memory using a tool called Pandas. It then bundles all these tables into a "dictionary" (a digital filing cabinet) and hands it back to the main program so the data is ready to be used.
