# ============================================================
# SCRIPT 08 — GEOGRAPHIC DISTRIBUTION
# Columns to drag into Values: country_primary, eif_commitment_eur
# ============================================================

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.patch.set_facecolor('#F4F6FB')

COLORS = ['#003399', '#0066CC', '#3399FF', '#66B2FF', '#99CCFF', '#CCE5FF']

# Left: count of fund managers by country
country_counts = dataset['country_primary'].value_counts()
bars = axes[0].bar(country_counts.index, country_counts.values,
                   color=COLORS[:len(country_counts)], edgecolor='white', linewidth=2)
for bar, val in zip(bars, country_counts.values):
    axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
                 str(int(val)), ha='center', fontsize=11, fontweight='bold', color='#333333')

axes[0].set_title('Fund Managers by Country', fontsize=12, fontweight='bold', color='#003399')
axes[0].set_ylabel('Number of Fund Managers', fontsize=10, color='#555555')
axes[0].set_ylim(0, country_counts.max() + 1.5)
axes[0].tick_params(axis='x', rotation=15, colors='#555555')
axes[0].spines['top'].set_visible(False)
axes[0].spines['right'].set_visible(False)
axes[0].set_facecolor('#F4F6FB')

# Right: total EIF commitment by country
country_commit = dataset.groupby('country_primary')['eif_commitment_eur'].sum().sort_values(ascending=False)
bars2 = axes[1].bar(country_commit.index, country_commit.values / 1e6,
                    color=COLORS[:len(country_commit)], edgecolor='white', linewidth=2)
for bar, val in zip(bars2, country_commit.values):
    axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                 f'€{val/1e6:.0f}M', ha='center', fontsize=9, fontweight='bold', color='#333333')

axes[1].set_title('Total EIF Commitment by Country (EUR M)', fontsize=12,
                  fontweight='bold', color='#003399')
axes[1].set_ylabel('EUR Millions', fontsize=10, color='#555555')
axes[1].tick_params(axis='x', rotation=15, colors='#555555')
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)
axes[1].set_facecolor('#F4F6FB')

plt.tight_layout()
plt.show()
