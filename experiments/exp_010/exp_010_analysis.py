import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Load results
csv_path = os.path.join(os.path.dirname(__file__), 'exp_010_results.csv')
df = pd.read_csv(csv_path)

# Calculate statistics
print("=== TIMING VALIDATION RESULTS ===")
print(f"Total runs: {len(df)}")
print(f"\nTiming Statistics:")
print(f"  Mean time: {df['time_s'].mean():.2f}s (expected: ~27.75s)")
print(f"  Std Dev: {df['time_s'].std():.2f}s")
print(f"  Min: {df['time_s'].min():.1f}s")
print(f"  Max: {df['time_s'].max():.1f}s")
print(f"  Moves/second: {df['moves_per_second'].mean():.3f}")

# Test hypothesis
expected = 27.75
actual = df['time_s'].mean()
error = abs(actual - expected) / expected * 100
print(f"\nHypothesis Test:")
print(f"  Expected: {expected}s")
print(f"  Actual: {actual:.2f}s")
print(f"  Error: {error:.1f}%")
print(f"  Result: {'✅ VALIDATED' if error < 10 else '❌ FAILED'}")

# Score statistics
print(f"\nScore Statistics:")
print(f"  Mean: {df['score'].mean():.1f}")
print(f"  Median: {df['score'].median()}")
print(f"  Max: {df['score'].max()}")

# Max tile distribution
print(f"\nMax Tile Distribution:")
tile_counts = df['max_tile'].value_counts().sort_index()
for tile, count in tile_counts.items():
    print(f"  {tile}: {count} ({count/len(df)*100:.1f}%)")

# Create visualization
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle(f'Experiment #010: Timing Validation ({len(df)} runs, 150 moves each)', fontsize=16)

# 1. Timing distribution with hypothesis line
ax1.hist(df['time_s'], bins=15, edgecolor='black', alpha=0.7, color='steelblue')
ax1.axvline(27.75, color='red', linestyle='--', linewidth=2, label='Hypothesis: 27.75s')
ax1.axvline(df['time_s'].mean(), color='green', linestyle='-', linewidth=2, 
            label=f'Actual: {df["time_s"].mean():.2f}s')
ax1.set_xlabel('Time (seconds)')
ax1.set_ylabel('Frequency')
ax1.set_title('Timing Distribution vs Hypothesis')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Score distribution
ax2.hist(df['score'], bins=20, edgecolor='black', alpha=0.7, color='darkgreen')
ax2.axvline(df['score'].mean(), color='red', linestyle='--', linewidth=2, 
            label=f'Mean: {df["score"].mean():.0f}')
ax2.set_xlabel('Score')
ax2.set_ylabel('Frequency')
ax2.set_title('Score Distribution (150 moves)')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 3. Timing consistency over runs
ax3.plot(df['run'], df['time_s'], 'o-', alpha=0.6, markersize=4)
ax3.axhline(27.75, color='red', linestyle='--', alpha=0.5, label='Expected')
ax3.fill_between(df['run'], 27.75-2, 27.75+2, alpha=0.2, color='red', label='±2s range')
ax3.set_xlabel('Run Number')
ax3.set_ylabel('Time (seconds)')
ax3.set_title('Timing Consistency')
ax3.legend()
ax3.grid(True, alpha=0.3)

# 4. Max tile distribution
tiles = sorted(df['max_tile'].unique())
counts = [len(df[df['max_tile'] == t]) for t in tiles]
ax4.bar(range(len(tiles)), counts, color='orange', edgecolor='black')
ax4.set_xticks(range(len(tiles)))
ax4.set_xticklabels(tiles)
ax4.set_xlabel('Max Tile')
ax4.set_ylabel('Count')
ax4.set_title('Max Tile Achievement')
ax4.grid(True, alpha=0.3, axis='y')

# Add percentage labels
for i, (tile, count) in enumerate(zip(tiles, counts)):
    ax4.text(i, count + 0.5, f'{count/len(df)*100:.0f}%', ha='center')

plt.tight_layout()
output_path = os.path.join(os.path.dirname(__file__), 'exp_010_validation.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"\nVisualization saved to: exp_010_validation.png")

# Compare with exp 009 (40 moves)
print("\n=== COMPARISON WITH EXP 009 (40 moves) ===")
print("Exp 009: 40 moves, mean time 6.46s = 0.162s/move")
print(f"Exp 010: 150 moves, mean time {df['time_s'].mean():.2f}s = {df['time_s'].mean()/150:.3f}s/move")
print(f"Timing model consistency: {'✅ Linear' if error < 10 else '❌ Non-linear'}")
