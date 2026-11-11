# Explanation of `src/visualization.py`

### What it does
This is the artist of the project. It takes all the raw numbers, math, and AI predictions and turns them into beautiful, easy-to-understand charts and graphs.

### The Logic Behind It
Humans are visual creatures. Staring at an Excel spreadsheet with 100,000 rows is impossible. This script uses drawing tools (like Matplotlib and Seaborn) to create pictures:
- **Histograms**: To show how many customers spend small amounts vs large amounts.
- **Bar Charts**: To show the top-selling product categories.
- **Scatter Plots**: To draw the customer clusters so we can actually see the different groups (like VIPs) separated in space.
- **Feature Importance Bars**: To visually show which clue (like delivery delay or review score) is the biggest cause of customers leaving.

Every time it draws a picture, it saves it as a PNG image file into the `outputs/plots` folder.
