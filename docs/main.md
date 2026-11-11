# Explanation of `main.py`

### What it does
This is the master script, the "CEO" or conductor of the entire project. When you want to run the project, this is the only file you actually execute.

### The Logic Behind It
If you look at the `src` folder, there are many different scripts doing very specific jobs. `main.py` is the script that links them all together in the correct logical order. 

Here is its step-by-step checklist:
1. Call `load_data.py` to get the raw data.
2. Pass that data to `preprocessing.py` to clean it up.
3. Pass the clean data to `rfm.py` and `clustering.py` to score and group the customers.
4. Run the advanced AI models by calling `clv_analysis.py` (future value), `churn_analysis.py` (who is leaving), and `nlp_analysis.py` (reading reviews).
5. Find product combinations by calling `fpgrowth_analysis.py`.
6. Finally, hand all the results over to `visualization.py` to draw the charts.
7. Print out a summary and business insights to the screen.

It ensures that output from Step 1 perfectly feeds into Step 2, and so on, until the whole data mining process is complete.
