# Comprehensive Final Report: Olist Data Mining & Customer Analytics

## 1. Executive Summary
This project presents an end-to-end data mining and machine learning pipeline applied to the **Olist Brazilian E-Commerce Public Dataset**. Over the course of the project, we evolved the pipeline from fundamental Exploratory Data Analysis (EDA) and RFM (Recency, Frequency, Monetary) clustering into an advanced predictive analytics engine. The final system accurately segments customers, forecasts Customer Lifetime Value (CLV), predicts churn, parses Portuguese review sentiments, and generates scalable cross-selling rules.

---

## 2. Goal of the Study
The primary objective of this project is to **transform raw, isolated transactional data into actionable, predictive business intelligence**. Specifically, the study aims to:
1. **Identify and segment** distinct customer profiles based on purchasing behavior to understand where revenue is concentrated.
2. **Diagnose and predict customer churn** by analyzing operational bottlenecks (e.g., delivery delays) and customer sentiment from reviews.
3. **Forecast future value** (Customer Lifetime Value) to help the business allocate marketing and retention budgets effectively.
4. **Discover hidden product synergies** (Market Basket Analysis) to drive cross-selling opportunities and increase the Average Order Value (AOV).

Ultimately, the goal is to provide a clear, data-driven strategy for transitioning Olist from an acquisition-heavy model to a **retention-focused, profitable e-commerce ecosystem**.

---

## 3. Project Roadmap & Evolution
The project was executed in a structured, multi-phase roadmap:

1. **Phase 1: Foundation & Clustering**
   - Implemented relational data merging across 100,000+ orders.
   - Built the RFM (Recency, Frequency, Monetary) model.
   - Segmented customers using K-Means Clustering ($K=4$), mathematically justified via Elbow and Silhouette metrics (Silhouette Score: **0.402**).
   - Generated 2D cluster maps via Principal Component Analysis (PCA).

2. **Phase 2: Predictive Machine Learning**
   - **Churn Prediction**: Built a Random Forest Classifier integrating operational data like delivery delays and review scores to predict customer attrition.
   - **CLV Forecasting**: Integrated the `lifetimes` package to deploy a Beta-Geometric/Negative Binomial Distribution (BG/NBD) model and a Gamma-Gamma model, predicting future purchasing frequency and monetary value.

3. **Phase 3: NLP & Advanced Market Basket Analysis**
   - **Review Sentiment Analysis**: Used TF-IDF and Logistic Regression to classify Portuguese customer reviews with **93.5% accuracy**.
   - **Topic Modeling**: Leveraged Non-Negative Matrix Factorization (NMF) to extract operational failure topics from negative reviews.
   - **Market Basket Optimization**: Replaced computationally expensive Apriori algorithms with the highly scalable **FP-Growth** algorithm to mine purchase patterns across the entire 112,000+ item dataset.

---

## 3. Architecture & Code Structure
The codebase was modularized to ensure maintainability and separation of concerns. The core logic resides in the `src/` directory, orchestrated by `main.py`.

### Core Pipeline Files
- `main.py`: The central orchestrator that runs the entire end-to-end data pipeline.
- `src/load_data.py`: Handles CSV ingestion and missing file checks.
- `src/preprocessing.py`: Executes complex table joins (Orders, Customers, Payments, Reviews) and handles missing dates.
- `src/rfm.py`: Transforms transactional logs into the customer-centric RFM matrix.

### Analytical & ML Modules
- `src/clustering.py`: Standardizes the RFM matrix and applies the K-Means algorithm. Includes mathematical validation metrics.
- `src/pca_analysis.py`: Compresses 3D spatial data into 2D visualizations.
- `src/clv_analysis.py`: Calculates probabilistic Customer Lifetime Value and expected purchase rates.
- `src/churn_analysis.py`: Trains the Random Forest model to predict churn, extracting feature importance.
- `src/nlp_analysis.py`: Processes natural language to determine review sentiment and extract text topics.
- `src/fpgrowth_analysis.py`: The FP-Growth Market Basket Analysis script identifying co-purchase lift.

### Output Architecture
- `outputs/models/`: Persists generated datasets and models (e.g., `customer_segments.csv`, `customer_clv_predictions.csv`, `fp_growth_association_rules.csv`).
- `outputs/plots/`: Stores all auto-generated visualizations (`pca_clusters.png`, `churn_feature_importance.png`, `cluster_validation.png`, `rfm_distributions.png`, etc.).

---

## 4. Key Findings & Data-Driven Analysis

### A. Customer Segmentation & The Retention Crisis
The K-Means clustering algorithm revealed a critical insight: **97% of Olist customers have only made a single purchase**. 
The segments break down as follows:
1. **Lost Low-Value Spenders (~43% of customers):** Purchased a long time ago, spent very little, and never returned.
2. **At-Risk High-Spenders (~37% of customers):** Made a single, high-value purchase but haven't returned in a long time. *Critically, this segment drives over 60% of total historical revenue.*
3. **New/Fresh Customers (~17% of customers):** Acquired recently. They are the immediate target for retention campaigns.
4. **Slipping Loyal Customers (~3% of customers):** The only segment showing repeat purchase behavior, but their recency indicates they are beginning to slip away.

> [!WARNING]
> **Business Action:** The company has an acquisition-heavy model but fails at retention. Priority must shift to post-purchase engagement targeting the "New/Fresh" and "At-Risk High-Spender" segments.

### B. Churn Prediction & Delivery Delays
The Random Forest churn model (ROC-AUC 0.615) highlighted that **average delivery delay** and **review scores** are strong predictive features for whether a customer will return. Poor delivery experiences directly correlate with negative reviews, which in turn permanently kill customer lifetime value.

### C. Natural Language Processing (NLP) of Reviews
Our NLP pipeline successfully classified reviews with 93.5% accuracy. By running Topic Modeling (NMF) exclusively on the negative reviews, we isolated the exact operational issues causing dissatisfaction. Fixing the themes highlighted in these topics (mostly surrounding delayed logistics and product mismatches) is a prerequisite to improving the retention rates identified in the RFM analysis.

### D. Market Basket Analysis (Product Synergies)
While the vast majority of carts contain only a single item, FP-Growth revealed specific cross-category synergies that have a positive Lift metric. For example, customers purchasing `home_confort` products show a significantly higher likelihood of buying `bed_bath_table` products. 

> [!TIP]
> **Business Action:** Use the FP-Growth association rules to build automated product recommendation carousels on the checkout page. Bundle these specific categories with slight discounts to increase the Average Order Value (AOV).

---

## 5. Conclusion
This data mining project transformed raw, relational transactional logs into actionable intelligence. By layering predictive analytics (CLV, Churn, NLP) on top of traditional EDA and clustering, we established a clear roadmap for Olist to improve its business: fix the delivery logistics driving negative sentiment, aggressively target the single-purchase high-spenders with retention campaigns, and leverage cross-selling bundles to extract more value per transaction.
