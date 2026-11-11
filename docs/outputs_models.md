# Explanation of `outputs/models` Directory

### What it is
This folder is the "save state" or the "memory bank" of the project. It stores the final results of all the heavy calculations as simple CSV (spreadsheet) files.

### The Logic Behind It
When the AI algorithms run (like clustering customers or predicting future spending), they take a lot of computer power and time. You don't want to run the math from scratch every single time you want to see the results.

Instead, once the scripts finish doing their math, they save their answers here.
- **`customer_segments.csv`**: A list of all customers and which "bucket" or VIP group they were placed into.
- **`customer_clv_predictions.csv`**: A list of all customers and the exact dollar amount the AI predicts they will spend next year.
- **`cluster_summary.csv`**: A summary table showing the average spending, frequency, and recency for each of the customer groups, along with their business names like "Champions" or "Lost Low-Value Spenders".
- **`fp_growth_association_rules.csv`** (and/or **`association_rules.csv`**): A spreadsheet of the rules found (e.g., "People buying X also buy Y").

By saving these, a business analyst can just open these spreadsheets in Excel and start using the insights immediately without writing any code.
