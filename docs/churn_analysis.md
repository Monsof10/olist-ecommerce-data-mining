# Explanation of `src/churn_analysis.py`

### What it does
This script trains an AI model to predict if a customer is about to "churn". Churning means a customer is going to stop using your business and never come back.

### The Logic Behind It
It defines a churned customer as someone who hasn't bought anything in the last 180 days. 

Then, it gives an AI algorithm called a "Random Forest" a bunch of clues about the customers. These clues include:
- How often they buy
- How much money they spend
- Their average review scores
- How many days their deliveries are usually delayed
- How they pay

The Random Forest acts like a detective. It looks at thousands of past customers who left and figures out the hidden patterns. For example, it might learn that "customers who experience a 10-day delivery delay and leave a bad review are 90% likely to never come back." Once trained, it can look at *current* customers and warn the business about who is most likely to leave today.
