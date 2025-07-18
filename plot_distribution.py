import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_score_distribution(score_file='outputs/scores.csv', output_image='outputs/score_distribution.png'):
    # Load score CSV
    df = pd.read_csv(score_file)

    # Bucket scores into ranges: 0–100, 100–200, ..., 900–1000
    df['score_range'] = pd.cut(df['credit_score'], bins=range(0, 1100, 100), right=False)

    # Count number of wallets per bucket
    score_counts = df['score_range'].value_counts().sort_index()

    # Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x=score_counts.index.astype(str), y=score_counts.values, palette='viridis')
    plt.title("Wallet Credit Score Distribution")
    plt.xlabel("Score Range")
    plt.ylabel("Number of Wallets")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_image)
    plt.show()

# Run if file is executed directly
if __name__ == "__main__":
    plot_score_distribution()
