import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load results
df = pd.read_csv('exp_008_results.csv')

# Basic statistics
print("=== SCORE STATISTICS ===")
print(f"Mean: {df['score'].mean():.1f}")
print(f"Median: {df['score'].median():.1f}")
print(f"Std Dev: {df['score'].std():.1f}")
print(f"Min: {df['score'].min()}")
print(f"Max: {df['score'].max()}")

# Max tile distribution
print("\n=== MAX TILE DISTRIBUTION ===")
tile_counts = df['max_tile'].value_counts().sort_index()
for tile, count in tile_counts.items():
    print(f"{tile}: {count/len(df)*100:.1f}%")

# Game over rate
game_over_rate = df['game_over'].sum() / len(df) * 100
print(f"\n=== GAME OVER RATE: {game_over_rate:.1f}% ===")

# UI/Memory match rate
match_rate = df['ui_memory_match'].sum() / len(df) * 100
print(f"\n=== UI/MEMORY MATCH RATE: {match_rate:.1f}% ===")

# Plot distribution
plt.figure(figsize=(10, 6))
plt.hist(df['score'], bins=20, alpha=0.7, edgecolor='black')
plt.axvline(df['score'].median(), color='red', linestyle='--', label=f'Median: {df["score"].median()}')
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.title('Score Distribution (100 runs, 150 moves each)')
plt.legend()
plt.savefig('exp_008/exp_008_distribution.png')
