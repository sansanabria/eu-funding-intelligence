# ============================================================
# SCRIPT 05 — PROJECT FIT COVERAGE
# Columns to drag into Values: manager_name, solar_fit,
#                               hydrogen_fit, desalination_fit
# ============================================================

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

dataset['short_name'] = dataset['manager_name'].apply(
    lambda x: x[:28] + '...' if len(str(x)) > 28 else x)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor('#F4F6FB')

# Left: summary bar chart
labels = ['Solar Energy', 'Green Hydrogen', 'Desalination /\nWater']
counts = [dataset['solar_fit'].sum(), dataset['hydrogen_fit'].sum(), dataset['desalination_fit'].sum()]
colors = ['#FFD700', '#003399', '#0066CC']

bars = axes[0].bar(labels, counts, color=colors, width=0.5, edgecolor='white', linewidth=2)
for bar, count in zip(bars, counts):
    axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                 f'{int(count)} funds', ha='center', fontsize=11, fontweight='bold', color='#333333')
axes[0].set_title('Funds Available by Project Type', fontsize=12, fontweight='bold', color='#003399')
axes[0].set_ylabel('Number of Fund Managers', fontsize=10, color='#555555')
axes[0].set_ylim(0, max(counts) + 2)
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)
axes[0].set_facecolor('#F4F6FB')

# Right: heatmap — which manager fits which project
fit_cols = ['solar_fit', 'hydrogen_fit', 'desalination_fit']
fit_labels = ['Solar', 'Hydrogen', 'Desalination']
d = dataset.set_index('short_name')[fit_cols]

im = axes[1].imshow(d.values, cmap='Blues', aspect='auto', vmin=0, vmax=1)
axes[1].set_xticks(range(3))
axes[1].set_xticklabels(fit_labels, fontsize=10)
axes[1].set_yticks(range(len(d.index)))
axes[1].set_yticklabels(d.index, fontsize=8)

for i in range(len(d.index)):
    for j in range(3):
        val = d.values[i, j]
        axes[1].text(j, i, '✓' if val == 1 else '', ha='center', va='center',
                     fontsize=14, color='white' if val == 1 else '#CCCCCC', fontweight='bold')

axes[1].set_title('Project Fit by Fund Manager', fontsize=12, fontweight='bold', color='#003399')
axes[1].set_facecolor('#F4F6FB')

plt.tight_layout()
plt.show()
