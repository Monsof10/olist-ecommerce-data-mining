# Explanation of `src/pca_analysis.py`

### What it does
This file takes complex data with many variables and simplifies it so it can be easily plotted on a flat 2D graph.

### The Logic Behind It
Imagine you have an object in 3D space, like a coffee mug, and you want to draw it on a flat piece of paper. You have to find the best angle to cast a shadow that still looks like a mug. 

PCA (Principal Component Analysis) does exactly this, but for data. If a customer is defined by 10 different numbers (their RFM scores, how many days they've been active, etc.), PCA mathematically squishes those 10 numbers down to just 2 numbers without losing the "shape" of the data. This allows us to draw a simple X and Y scatter plot of all our customers so humans can see the clusters visually.
