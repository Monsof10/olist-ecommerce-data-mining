# Explanation of `outputs/plots` Directory

### What it is
This folder is the project's photo album. It contains all the images (PNG files) of the charts and graphs that the project created.

### The Logic Behind It
While the `models` folder contains the hard numbers (spreadsheets), the `plots` folder contains the visual stories. The `visualization.py` script takes the numbers and draws pictures, then saves them here.

When you open this folder, you will find pictures like:
- **`rfm_distributions.png`**: A chart showing if most people buy recently or haven't bought in a long time.
- **`pca_clusters.png`**: A beautiful scatter plot showing the different customer groups as different colored dots.
- **`top_products.png`**: A bar chart of the best-selling items in your store.
- **`churn_feature_importance.png`**: A chart showing which factors (like bad reviews or slow shipping) most cause a customer to leave.
- **`association_rules.png`**: A bubble chart that shows how strong the connection is between products bought together (e.g., if you buy a console, you definitely buy a controller).
- **`clv_distribution.png`**: A curve showing how much money the majority of your customers are expected to spend in their lifetime.
- **`cluster_validation.png`**: Line graphs (Elbow and Silhouette) that prove the AI chose the right number of groups (like 4 clusters) to divide your customers into.
- **`review_topics.png`**: Bar charts that show the most common words people use when leaving a negative review, making it easy to spot problems like "delivery delay".

These images are perfect to be copied and pasted directly into a PowerPoint presentation for a business meeting.
