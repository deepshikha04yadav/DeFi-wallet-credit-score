from feature_engineering import extract_features
from normalize_and_model import normalize_features, score_wallets
import json

# Load raw data
with open('data/user-wallet-transactions.json') as f:
    transactions = json.load(f)

# Step 1: Feature extraction
df_features = extract_features(transactions)

# Step 2: Normalize
df_scaled, scaler = normalize_features(df_features)

# Step 3: Score
df_scores, model = score_wallets(df_scaled)

# Save results
df_scores.to_csv('outputs/scores.csv', index=False)
print(df_scores.head())
