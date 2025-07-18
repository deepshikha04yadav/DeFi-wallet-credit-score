import pandas as pd
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import IsolationForest
import numpy as np

def normalize_features(df):
    feature_cols = [
        'total_tx', 'active_days', 'deposit_count', 'borrow_count', 'repay_count',
        'redeem_count', 'liquidation_count', 'repay_ratio',
        'liquidation_ratio', 'borrow_to_deposit'
    ]

    scaler = RobustScaler()
    scaled_features = scaler.fit_transform(df[feature_cols])
    df_scaled = pd.DataFrame(scaled_features, columns=feature_cols)
    df_scaled['wallet'] = df['wallet'].values
    return df_scaled, scaler


def score_wallets(df_scaled, model=None):
    feature_cols = [col for col in df_scaled.columns if col != 'wallet']

    if model is None:
        model = IsolationForest(contamination=0.05, random_state=42)

    model.fit(df_scaled[feature_cols])
    anomaly_scores = model.decision_function(df_scaled[feature_cols])  # the higher, the better
    anomaly_scores = (anomaly_scores - anomaly_scores.min()) / (anomaly_scores.max() - anomaly_scores.min())
    credit_scores = (anomaly_scores * 1000).astype(int)

    df_result = pd.DataFrame({
        'wallet': df_scaled['wallet'],
        'credit_score': credit_scores
    }).sort_values(by='credit_score', ascending=False)

    return df_result, model
