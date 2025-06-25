import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load results
df = pd.read_csv('exp_009_deep_results.csv')

# Create figure with subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('2048 Deep Run Analysis: 100 runs, 40 moves each', fontsize=16)

# 1. Score distribution histogram
ax1.hist(df['score'], bins=20, edgecolor='black', alpha=0.7, color='steelblue')
ax1.axvline(df['score'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["score"].mean():.1f}')
ax1.axvline(df['score'].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {df["score"].median():.1f}')
ax1.set_xlabel('Score')
ax1.set_ylabel('Frequency')
ax1.set_title('Score Distribution')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Timing distribution histogram
ax2.hist(df['time_s'], bins=15, edgecolor='black', alpha=0.7, color='darkgreen')
ax2.axvline(df['time_s'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["time_s"].mean():.2f}s')
ax2.set_xlabel('Time (seconds)')
ax2.set_ylabel('Frequency')
ax2.set_title('Timing Distribution')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 3. Score vs Run Number (to check for patterns)
ax3.scatter(df['run'], df['score'], alpha=0.6, s=30)
ax3.plot(df['run'], df['score'].rolling(10).mean(), color='red', linewidth=2, label='10-run moving avg')
ax3.set_xlabel('Run Number')
ax3.set_ylabel('Score')
ax3.set_title('Score Progression')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 4. Max tile distribution
tile_counts = df['max_tile'].value_counts().sort_index()
ax4.bar(tile_counts.index.astype(str), tile_counts.values, color='orange', edgecolor='black')
ax4.set_xlabel('Max Tile')
ax4.set_ylabel('Count')
ax4.set_title('Max Tile Distribution')
ax4.grid(True, alpha=0.3, axis='y')

# Add percentage labels on bars
for i, (tile, count) in enumerate(tile_counts.items()):
    ax4.text(i, count + 0.5, f'{count/len(df)*100:.1f}%', ha='center')

plt.tight_layout()
plt.savefig('exp_009_deep_analysis.png', dpi=150, bbox_inches='tight')

# Print detailed statistics
print("=== DETAILED STATISTICS ===")
print(f"\nScore Statistics:")
print(f"  Mean: {df['score'].mean():.2f}")
print(f"  Std Dev: {df['score'].std():.2f}")
print(f"  Median: {df['score'].median()}")
print(f"  Q1: {df['score'].quantile(0.25)}")
print(f"  Q3: {df['score'].quantile(0.75)}")

print(f"\nTiming Statistics:")
print(f"  Mean: {df['time_s'].mean():.3f}s")
print(f"  Std Dev: {df['time_s'].std():.3f}s")
print(f"  Min: {df['time_s'].min():.3f}s")
print(f"  Max: {df['time_s'].max():.3f}s")

print(f"\nMax Tile Distribution:")
for tile, count in tile_counts.items():
    print(f"  {tile}: {count} ({count/len(df)*100:.1f}%)")
