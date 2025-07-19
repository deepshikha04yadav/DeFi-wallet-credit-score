# Defi-wallet-credit-score

# 🏦 DeFi Wallet Credit Scoring – Aave V2 Protocol

This project builds a robust pipeline to assign **credit scores (0–1000)** to wallets based on historical transaction behavior with the Aave V2 protocol.

The goal is to distinguish responsible users from risky or bot-like actors using only raw DeFi transaction data.

---

## 📦 Dataset

- Source: [Aave V2 Protocol - Raw Wallet Transactions](https://drive.google.com/file/d/1ISFbAXxadMrt7Zl96rmzzZmEKZnyW7FS/view?usp=sharing)
- Format: JSON file (~87MB) of 100K+ wallet transactions
- Actions include:
  - `deposit`, `borrow`, `repay`, `redeemunderlying`, `liquidationcall`

---

## ⚙️ Architecture & Processing Flow
```bash
  ┌────────────────────────────┐
  │Raw JSON (user-transactions)│
  └────────────┬───────────────┘
               ▼
 [1] Extract features per wallet (feature_engineering.py)
               ▼
 [2] Normalize features using RobustScaler
               ▼
 [3] Score wallets with IsolationForest (risk → score)
               ▼
 [4] Output: scores.csv (walletAddress, credit_score)
```

---

## 🧠 Feature Engineering

Each wallet is represented by behavior-based features such as:

- `total_tx`, `active_days`
- Action counts: `deposit_count`, `borrow_count`, `repay_count`
- Risk metrics: `liquidation_count`, `liquidation_ratio`
- Financial ratios: `repay_ratio`, `borrow_to_deposit`

---

## 🤖 Model

- **Model:** Unsupervised [Isolation Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)
- **Output:** Anomaly score → scaled to 0–1000 credit score
- **Assumption:** Higher anomalies = higher risk = lower score

---

## 🚀 How to Run

### ⚙️ Requirements

```bash
pip install -r requirements.txt
```

### 🏁 One-Step Scoring
```bash
python score_wallets.py --input data/user-wallet-transactions.json --output outputs/scores.csv
```

  --input: path to the raw JSON file

  --output: path to output credit scores CSV

## 📊 Analysis
See analysis.md for:

  Credit score distribution
  Common traits of high- and low-scoring wallets
  Statistical summaries

## 📁 Repository Structure
```bash
aave-wallet-credit-scoring/
├── data/  
│   └── user-wallet-transactions.json                       # Input JSON
├── outputs/                                     # Scored CSV + plots
│   ├── score_distribution.png
│   ├── scores.csv
│   └── wallet_features.csv                  
├── feature_engineering.py
├── normalize_and_model.py
├── plot_distribution.py
├── score_wallets.py    
├── eda.ipynb          # Main entry script
├── analysis.md
├── README.md
└── requirements.txt
```
## 📌 Future Work
Incorporate time-weighted features

Label-based (supervised) scoring if loan defaults become observable

Include flash loan patterns or MEV detections

## 🧑‍💻 Author
This project was built as a proof of concept for credit scoring in decentralized finance using purely behavioral on-chain data.
