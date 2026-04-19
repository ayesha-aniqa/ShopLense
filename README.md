# 🛍️ ShopLens — Know Your Customers, Grow Your Business

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)

---

## 📌 Project Overview

Most online businesses treat all customers the same way — same emails, same discounts, same offers. This wastes money and drives customers away.

**ShopLens** solves this by automatically grouping customers based on their real shopping behavior using **RFM Analysis** (Recency, Frequency, Monetary value) — one of the most trusted methods used by real businesses worldwide.

The system goes one step further — it can predict which group a **brand new customer** belongs to, based on just their first 2–3 purchases. This allows businesses to act early and send the right message at the right time.

---

## 🎯 Problem Statement

Given a dataset of real e-commerce transactions, can we:
1. Automatically group existing customers into meaningful segments?
2. Predict which segment a new customer will fall into from their early purchases?
3. Recommend a marketing action for each customer segment?

---

## 🗂️ Dataset

- **Name:** Online Retail II
- **Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
- **Size:** 1M+ transactions from a real UK-based online retailer
- **Period:** 2009 – 2011
- **Features:** InvoiceNo, StockCode, Description, Quantity, InvoiceDate, Price, CustomerID, Country

---

## 🧠 Models Used

| Model | Type | Purpose |
|---|---|---|
| K-Means | ML — Clustering | Group customers into segments |
| DBSCAN | ML — Clustering | Compare with K-Means, remove noise |
| Autoencoder | DL — Neural Network | Compress features before clustering |
| Random Forest | ML — Classifier | Predict segment for new customers |

---

## 🏗️ Project Workflow
```
https://githubusercontent.com[Your-Username]/[Your-Repo-Name]/main/reports/flowchart.jpg
```

---

## 📁 Folder Structure
```
shoplens/
├── app/
│   ├── main.py               # Streamlit entry point
│   ├── predict.py            # Prediction pipeline
│   ├── utils.py              # Helper functions
│   └── components.py         # UI chart components
├── data/
│   ├── raw/                  # Original downloaded CSV
│   ├── processed/            # Cleaned RFM dataset
│   └── sample/               # Small sample for testing
├── models/
│   ├── kmeans_model.pkl      # Trained K-Means
│   ├── autoencoder_model.pkl  # Trained Autoencoder
│   └── classifier_rf.pkl     # Trained Random Forest
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_clustering.ipynb
│   ├── 04_autoencoder.ipynb
│   └── 05_classifier.ipynb
├── reports/
│   ├── (Auto-generated Visuals)
│   └── presentation_slides.pdf
├── .gitignore
├── LICENSE
├── PROGRESS.md
├── README.md
└── requirements.txt
```

---

## 📊 Customer Segments

| Segment | Description | Action |
|---|---|---|
| 👑 Champions | Bought recently, buy often, spend the most | Reward them |
| 💛 Loyal Customers | Buy regularly with good spending | Upsell premium products |
| 🌱 New Customers | Bought recently but not yet often | Onboard and nurture |
| ⚠️ At Risk | Used to buy often but haven't recently | Send win-back offers |
| 💤 Lost Customers | Haven't bought in a long time | Last-chance discount |

---

## 🚀 How to Run Locally

**1. Clone the repository**
```bash
https://github.com/ayesha-aniqa/ShopLense.git
cd shoplens
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the Streamlit app**
```bash
python -m streamlit run app/main.py
```

**4. Open in browser**
```
http://localhost:8501
```

---

## 🌐 Live Demo

🔗 [Click here to open ShopLens](https://shoplense-uajvuijwwtzy3wgermg9ae.streamlit.app/)

---

## 📝 Medium Article

📖 [Read the full project walkthrough]() — *link will be added after publishing*

---

## 📈 Results

| Model | Metric | Score |
|---|---|---|
| K-Means | Silhouette Score | *0.4737* |
| DBSCAN | Silhouette Score | *0.6451* |
| Random Forest | Accuracy | *0.9816* |
| Random Forest | F1 Score | *0.98* |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10 | Core language |
| Pandas | Data manipulation |
| Scikit-learn | ML models |
| Pickle | Autoencoder |
| Streamlit | Web application |
| Plotly | Interactive charts |
| SHAP | Model explainability |
| GitHub Actions | Cloud deployment |

---

## 👤 Author

**Ayesha Aniqa**
AI/ML Fellowship 
📧 codeaisha123@gmail.com
🔗 [LinkedIn](in/ayesha-aniqa-342220282)
🐙 [GitHub](https://github.com/ayesha-aniqa)
📖 [Medium](https://medium.com/@codeaisha123)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
