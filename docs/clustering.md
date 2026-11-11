# Explanation of `src/clustering.py`

### What it does
This file groups your customers into different "clusters" or buckets based on their shopping habits.

### The Logic Behind It
Once we know every customer's RFM score (Recency, Frequency, Monetary), we have thousands of customers with different numbers. It's too hard to look at them one by one. 

1. **Normalization**: First, it scales all the numbers so they are fair to compare. (For example, spending $100 shouldn't overshadow visiting the store 5 times).
2. **K-Means Algorithm**: It uses an Artificial Intelligence algorithm called "K-Means". You tell it "I want to divide my customers into 4 groups", and the algorithm automatically figures out the best way to group similar customers together. 
3. **Validation**: It checks its own math to make sure the groups it created actually make sense (using something called an "Elbow Method" and "Silhouette Score").

In the end, you get neat labels for your customers, like "VIPs", "Lost Customers", or "Newbies".
