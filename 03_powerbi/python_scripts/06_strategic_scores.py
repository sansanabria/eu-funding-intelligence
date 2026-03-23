# ============================================================
# SCRIPT 06 — STRATEGIC FIT SCORES RANKING
# Columns to drag into Values: manager_name, score_project_fit,
#   score_commitment, score_sdg, score_contact,
#   score_geography, fit_score_10, priority_tier
# ============================================================

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

dataset['short_name'] = dataset['manager_name'].apply(
    lambda x: x[:28] + '...' if len(str(x)) > 28 else x)

df_s = dataset.sort_values('fit_score_10', ascending=True).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor('#F4F6FB')
ax.set_facecolor('#F4F6FB')

score_cols   = ['score_project_fit', 'score_commitment', 'score_sdg', 'score_contact', 'score_geography']
score_labels = ['Project Fit', 'EIF Commitment', 'SDG Alignment', 'Contact Info', 'Geography']
colors       = ['#003399', '#0066CC', '#3399FF', '#66B2FF', '#99CCFF']

bottoms = np.zeros(len(df_s))
for col, label, color in zip(score_cols, score_labels, colors):
    vals = pd.to_numeric(df_s[col], errors='coerce').fillna(0).values
    ax.barh(df_s['short_name'], vals, left=bottoms, label=label,
            color=color, edgecolor='white', linewidth=0.5, height=0.6)
    bottoms += vals

# Score labels + tier badges
tier_colors = {'Tier 1 - Priority': '#00AA44', 'Tier 2 - Secondary': '#FF9900', 'Tier 3 - Monitor': '#CC0000'}
for i, row in df_s.iterrows():
    score = row['fit_score_10']
    tier  = row.get('priority_tier', '')
    color = tier_colors.get(tier, '#555555')
    ax.text(score + 0.15, i, f'{score}/10', va='center', fontsize=9, color='#333333', fontweight='bold')
    ax.text(-0.5, i, '●', va='center', ha='right', fontsize=12, color=color)

ax.set_title('Strategic Fit Score — Fund Manager Ranking', fontsize=13,
             fontweight='bold', color='#003399', pad=15)
ax.set_xlabel('Score (out of 10)', fontsize=10, color='#555555')
ax.set_xlim(-1, 13)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#CCCCCC')
ax.spines['bottom'].set_color('#CCCCCC')
ax.tick_params(colors='#555555')

legend_handles = [mpatches.Patch(color=c, label=l) for c, l in zip(colors, score_labels)]
tier_handles   = [mpatches.Patch(color=c, label=t) for t, c in tier_colors.items()]
ax.legend(handles=legend_handles + tier_handles, loc='lower right', fontsize=8,
          framealpha=0.9, ncol=2)

plt.tight_layout()
plt.show()
