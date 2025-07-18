import json
import pandas as pd
from tqdm import tqdm
from collections import defaultdict

def extract_features(transactions):
    wallet_stats = defaultdict(lambda: {
        'total_tx': 0,
        'actions': defaultdict(int),
        'total_amounts': defaultdict(float),
        'first_ts': float('inf'),
        'last_ts': 0,
        'liquidation_count': 0,
        'borrow_amount': 0.0,
        'repay_amount': 0.0,
    })

    for tx in tqdm(transactions, desc="Extracting Features"):
        wallet = tx.get('userWallet')
        action = tx.get('action')
        action_data = tx.get('actionData', {})
        timestamp = int(tx.get('timestamp', 0))

        # Parse amount and normalize to float (handle non-numeric errors safely)
        try:
            amount = float(action_data.get('amount', 0)) / 1e6
        except:
            amount = 0.0

        stats = wallet_stats[wallet]
        stats['total_tx'] += 1
        stats['actions'][action] += 1
        stats['total_amounts'][action] += amount
        stats['first_ts'] = min(stats['first_ts'], timestamp)
        stats['last_ts'] = max(stats['last_ts'], timestamp)

        if action == 'liquidationcall':
            stats['liquidation_count'] += 1
        if action == 'borrow':
            stats['borrow_amount'] += amount
        if action == 'repay':
            stats['repay_amount'] += amount

    # Convert stats to DataFrame
    rows = []
    for wallet, stats in wallet_stats.items():
        active_days = max(1, (stats['last_ts'] - stats['first_ts']) // 86400)
        repay_ratio = stats['repay_amount'] / stats['borrow_amount'] if stats['borrow_amount'] > 0 else 1.0
        liquidation_ratio = stats['liquidation_count'] / stats['total_tx']
        borrow_to_deposit = stats['total_amounts']['borrow'] / stats['total_amounts']['deposit'] if stats['total_amounts']['deposit'] > 0 else 0.0

        row = {
            'wallet': wallet,
            'total_tx': stats['total_tx'],
            'active_days': active_days,
            'deposit_count': stats['actions']['deposit'],
            'borrow_count': stats['actions']['borrow'],
            'repay_count': stats['actions']['repay'],
            'redeem_count': stats['actions']['redeemunderlying'],
            'liquidation_count': stats['liquidation_count'],
            'repay_ratio': repay_ratio,
            'liquidation_ratio': liquidation_ratio,
            'borrow_to_deposit': borrow_to_deposit,
        }
        rows.append(row)

    return pd.DataFrame(rows)
