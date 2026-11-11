# Explanation of `src/clv_analysis.py`

### What it does
This script predicts the "Customer Lifetime Value" (CLV). It tries to guess exactly how much money each customer is going to spend at your store over the next 12 months.

### The Logic Behind It
To predict the future, this code uses advanced statistical models (with scary names like BG/NBD and Gamma-Gamma). 

But the logic is simple: 
1. **BG/NBD Model**: It looks at a customer's past purchases to guess *how many more times* they will come back to buy something in the next year. It also guesses if the customer is "alive" (still active) or "dead" (moved on to a competitor).
2. **Gamma-Gamma Model**: It looks at how much the customer usually spends and guesses what their *average bill* will be in the future.

It multiplies these two guesses together (Number of future visits * Average bill) to give you a dollar amount: the Customer's Lifetime Value.
