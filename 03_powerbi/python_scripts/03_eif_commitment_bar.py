# ============================================================
# SCRIPT 03 — EIF COMMITMENT BY FUND MANAGER
# Columns to drag into Values: manager_name, eif_commitment_eur
# ============================================================

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

d = dataset.dropna(subset=['eif_commitment_eur']).sort_values('eif_commitment_eur', ascending=True)
d['short_name'] = d['manager_name'].apply(lambda x: x[:30] + '...' if len(str(x)) > 30 else x)

fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor('#F4F6FB')
ax.set_facecolor('#F4F6FB')

colors = ['#003399' if v >= 40e6 else '#0066CC' if v >= 20e6 else '#3399FF'
          for v in d['eif_commitment_eur']]

bars = ax.barh(d['short_name'], d['eif_commitment_eur'] / 1e6,
               color=colors, edgecolor='white', linewidth=0.5, height=0.6)

for bar, val in zip(bars, d['eif_commitment_eur']):
    ax.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height() / 2,
            f'EUR {val/1e6:.1f}M', va='center', fontsize=9, color='#333333')

ax.set_title('EIF Commitment by Fund Manager', fontsize=13, fontweight='bold',
             color='#003399', pad=15)
ax.set_xlabel('EUR Millions', fontsize=10, color='#555555')
ax.tick_params(colors='#555555')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#CCCCCC')
ax.spines['bottom'].set_color('#CCCCCC')

from matplotlib.patches import Patch
legend = [Patch(color='#003399', label='≥ EUR 40M'),
          Patch(color='#0066CC', label='EUR 20M–40M'),
          Patch(color='#3399FF', label='< EUR 20M')]
ax.legend(handles=legend, loc='lower right', fontsize=9, framealpha=0.8)

plt.tight_layout()
plt.show()
