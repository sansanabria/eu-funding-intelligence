# ============================================================
# SCRIPT 07 — SDG ALIGNMENT HEATMAP
# Columns to drag into Values: manager_name, sdg_tags
# ============================================================

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

dataset['short_name'] = dataset['manager_name'].apply(
    lambda x: x[:28] + '...' if len(str(x)) > 28 else x)

# Build SDG matrix
all_sdgs = []
for tags in dataset['sdg_tags'].dropna():
    for s in str(tags).split(','):
        s = s.strip()
        if s.isdigit():
            all_sdgs.append(int(s))
all_sdgs = sorted(set(all_sdgs))

sdg_cols = [f'SDG {s}' for s in all_sdgs]
matrix = pd.DataFrame(0, index=dataset['short_name'], columns=sdg_cols)

for _, row in dataset.iterrows():
    name = row['short_name']
    if pd.notna(row['sdg_tags']) and row['sdg_tags']:
        for s in str(row['sdg_tags']).split(','):
            s = s.strip()
            if s.isdigit() and f'SDG {s}' in matrix.columns:
                matrix.loc[name, f'SDG {s}'] = 1

fig, ax = plt.subplots(figsize=(13, 7))
fig.patch.set_facecolor('#F4F6FB')
ax.set_facecolor('#F4F6FB')

im = ax.imshow(matrix.values, cmap='Blues', aspect='auto', vmin=0, vmax=1.2)

# Checkmarks
for i in range(len(matrix.index)):
    for j in range(len(matrix.columns)):
        if matrix.values[i, j] == 1:
            ax.text(j, i, '✓', ha='center', va='center',
                    fontsize=13, color='white', fontweight='bold')

# SDG color stripe at top
sdg_colors = {6:'#26BDE2', 7:'#FCC30B', 9:'#FD6925', 13:'#3F7E44', 14:'#0A97D9'}
for j, sdg_num in enumerate(all_sdgs):
    color = sdg_colors.get(sdg_num, '#003399')
    ax.add_patch(plt.Rectangle((j-0.5, -0.9), 1, 0.5, color=color, clip_on=False))

ax.set_xticks(range(len(sdg_cols)))
ax.set_xticklabels(sdg_cols, rotation=45, ha='right', fontsize=9, color='#333333')
ax.set_yticks(range(len(matrix.index)))
ax.set_yticklabels(matrix.index, fontsize=9, color='#333333')
ax.set_title('SDG Alignment by Fund Manager', fontsize=13,
             fontweight='bold', color='#003399', pad=20)

# Legend
legend = [mpatches.Patch(color='#26BDE2', label='SDG 6 — Clean Water'),
          mpatches.Patch(color='#FCC30B', label='SDG 7 — Renewable Energy'),
          mpatches.Patch(color='#FD6925', label='SDG 9 — Industry & Innovation'),
          mpatches.Patch(color='#3F7E44', label='SDG 13 — Climate Action'),
          mpatches.Patch(color='#0A97D9', label='SDG 14 — Life Below Water')]
ax.legend(handles=legend, loc='lower right', fontsize=8,
          bbox_to_anchor=(1.0, -0.35), ncol=3, framealpha=0.9)

plt.tight_layout()
plt.show()
