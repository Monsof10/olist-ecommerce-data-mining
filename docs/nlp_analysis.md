# Explanation of `src/nlp_analysis.py`

### What it does
This file uses Artificial Intelligence to read and understand customer reviews written in text. It figures out if the customer is happy or angry, and what exactly they are complaining about.

### The Logic Behind It
Computers can't read text like humans do, so this script (which does Natural Language Processing, or NLP) acts as a translator:
1. **Sentiment Analysis**: It trains a model to figure out if a review is Positive or Negative. It looks at the stars the customer gave (1-2 is negative, 4-5 is positive) and learns which words are associated with anger or happiness.
2. **Topic Modeling**: It isolates all the negative reviews. Then, it uses an algorithm called NMF to group the angry reviews into common themes. If it sees the words "late", "never arrived", and "slow" together a lot, it groups them into a "Delivery Issues" topic. This tells the business exactly *why* people are upset without having to read thousands of reviews manually.
