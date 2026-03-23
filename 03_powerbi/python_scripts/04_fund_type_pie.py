# ============================================================
# SCRIPT 04 — FUND TYPE DISTRIBUTION
# Columns to drag into Values: fund_type, eif_commitment_eur
# ============================================================

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

fig, axes = plt.subplots(1, 2, figsize=(13, 6))
fig.patch.set_facecolor('#F4F6FB')

COLORS = ['#003399', '#0066CC', '#3399FF', '#66B2FF', '#99CCFF', '#FFD700']

# Left: count of fund managers by type
type_counts = dataset['fund_type'].value_counts()
wedges, texts, autotexts = axes[0].pie(
    type_counts.values,
    labels=type_counts.index,
    autopct='%1.0f%%',
    colors=COLORS[:len(type_counts)],
    startangle=90,
    wedgeprops=dict(edgecolor='white', linewidth=2)
)
for text in autotexts:
    text.set_fontsize(10)
    text.set_fontweight('bold')
    text.set_color('white')
axes[0].set_title('Fund Managers by Type\n(Count)', fontsize=12,
                  fontweight='bold', color='#003399')

# Right: EIF commitment by fund type
type_commit = dataset.groupby('fund_type')['eif_commitment_eur'].sum().sort_values(ascending=True)
bars = axes[1].barh(type_commit.index, type_commit.values / 1e6,
                    color=COLORS[:len(type_commit)], edgecolor='white', linewidth=0.5)
for bar, val in zip(bars, type_commit.values):
    axes[1].text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                 f'EUR {val/1e6:.1f}M', va='center', fontsize=9, color='#333333')

axes[1].set_title('EIF Commitment by Fund Type\n(EUR Millions)', fontsize=12,
                  fontweight='bold', color='#003399')
axes[1].set_xlabel('EUR Millions', fontsize=10, color='#555555')
axes[1].spines['top'].set_visible(False)
axes[1].spines['right'].set_visible(False)
axes[1].set_facecolor('#F4F6FB')

plt.tight_layout()
plt.show()
