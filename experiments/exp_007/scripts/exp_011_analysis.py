import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

# Load data
base_dir = os.path.dirname(__file__)
curve_df = pd.read_csv(os.path.join(base_dir, '../exp_011_timing_curve.csv'))
phases_df = pd.read_csv(os.path.join(base_dir, '../exp_011_phases.csv'))
density_df = pd.read_csv(os.path.join(base_dir, '../exp_011_density.csv'))

# Aggregate timing curve data
timing_stats = curve_df.groupby('moves').agg({
    'time_s': ['mean', 'std'],
    'score': 'mean'
}).reset_index()
timing_stats.columns = ['moves', 'mean_time', 'std_time', 'mean_score']
timing_stats['ms_per_move'] = timing_stats['mean_time'] / timing_stats['moves'] * 1000

# Define curve fitting functions
def linear_model(x, a, b):
    return a + b * x

def log_model(x, a, b, c):
    return a + b * x + c * np.log(x)

def startup_model(x, startup, per_move):
    return startup + per_move * x

# Fit models
moves = timing_stats['moves'].values
times = timing_stats['mean_time'].values

# Fit different models
popt_linear, _ = curve_fit(linear_model, moves, times)
popt_log, _ = curve_fit(log_model, moves, times)
popt_startup, _ = curve_fit(startup_model, moves, times)

# Create visualization
fig = plt.figure(figsize=(15, 12))

# 1. Timing curve with fitted models
ax1 = plt.subplot(2, 2, 1)
ax1.errorbar(timing_stats['moves'], timing_stats['mean_time'], 
             yerr=timing_stats['std_time'], fmt='o', label='Measured', capsize=5)

x_fit = np.linspace(10, 200, 100)
ax1.plot(x_fit, linear_model(x_fit, *popt_linear), '--', label=f'Linear: {popt_linear[0]:.2f} + {popt_linear[1]:.3f}*moves')
ax1.plot(x_fit, log_model(x_fit, *popt_log), '-', label=f'Log model', linewidth=2)
ax1.plot(x_fit, startup_model(x_fit, *popt_startup), ':', 
         label=f'Startup: {popt_startup[0]:.2f}s + {popt_startup[1]:.3f}s/move')

ax1.set_xlabel('Number of Moves')
ax1.set_ylabel('Total Time (seconds)')
ax1.set_title('Timing Curve Analysis')
ax1.legend()
ax1.grid(True, alpha=0.3)

# 2. Per-move timing
ax2 = plt.subplot(2, 2, 2)
ax2.plot(timing_stats['moves'], timing_stats['ms_per_move'], 'o-', markersize=8)
ax2.axhline(y=160, color='r', linestyle='--', label='Expected 160ms/move')
ax2.set_xlabel('Number of Moves')
ax2.set_ylabel('Time per Move (ms)')
ax2.set_title('Per-Move Timing vs Total Moves')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 3. Game phases analysis
ax3 = plt.subplot(2, 2, 3)
if len(phases_df) > 0:
    phases_df['ms_per_move'] = phases_df['time_s'] / phases_df['moves'] * 1000
    ax3.bar(phases_df['phase'], phases_df['ms_per_move'], color=['green', 'orange', 'red'])
    ax3.set_ylabel('Time per Move (ms)')
    ax3.set_title('Timing by Game Phase')
    
    # Add tile count as text on bars
    for i, (phase, tiles) in enumerate(zip(phases_df['phase'], phases_df['tiles_on_board'])):
        ax3.text(i, phases_df['ms_per_move'].iloc[i] + 5, f'{tiles} tiles', ha='center')

# 4. Board density impact
ax4 = plt.subplot(2, 2, 4)
if len(density_df) > 0:
    density_df['ms_per_move'] = density_df['time_s'] / density_df['moves'] * 1000
    colors = {'corner': 'darkred', 'spread': 'lightblue', 'standard': 'green'}
    for strategy in density_df['strategy'].unique():
        data = density_df[density_df['strategy'] == strategy]
        ax4.bar(strategy, data['ms_per_move'].values[0], color=colors[strategy])
        ax4.text(strategy, data['ms_per_move'].values[0] + 2, 
                f"{data['tiles'].values[0]} tiles", ha='center')
    ax4.set_ylabel('Time per Move (ms)')
    ax4.set_title('Board Density Impact on Timing')

plt.tight_layout()
output_path = os.path.join(base_dir, '../exp_011_analysis.png')
plt.savefig(output_path, dpi=150, bbox_inches='tight')

# Print analysis results
print("=== TIMING CURVE ANALYSIS ===")
print(f"\nLinear model: time = {popt_linear[0]:.2f} + {popt_linear[1]:.3f} * moves")
print(f"  Startup overhead: {popt_linear[0]:.2f}s")
print(f"  Per-move cost: {popt_linear[1]*1000:.1f}ms")

print(f"\nStartup model: time = {popt_startup[0]:.2f} + {popt_startup[1]:.3f} * moves")
print(f"  Fixed startup: {popt_startup[0]:.2f}s")
print(f"  Consistent per-move: {popt_startup[1]*1000:.1f}ms")

print("\nPer-move timing by move count:")
for _, row in timing_stats.iterrows():
    print(f"  {row['moves']} moves: {row['ms_per_move']:.1f}ms/move")

print("\n=== KEY FINDINGS ===")
startup_effect = (timing_stats.iloc[0]['ms_per_move'] - timing_stats.iloc[-1]['ms_per_move']) / timing_stats.iloc[0]['ms_per_move'] * 100
print(f"1. Startup effect: {startup_effect:.1f}% decrease from 10 to 200 moves")
print(f"2. Optimal batch size for experiments: 100+ moves")
print(f"3. True per-move cost after startup: ~{timing_stats.iloc[-1]['ms_per_move']:.0f}ms")
