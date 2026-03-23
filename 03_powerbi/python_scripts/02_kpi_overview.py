# ============================================================
# SCRIPT 02 — KPI OVERVIEW
# Columns to drag into Values: ALL columns
# Shows: Total funds, countries, EIF capital, top fund
# ============================================================

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

fig, axes = plt.subplots(2, 3, figsize=(14, 6))
fig.patch.set_facecolor('#F4F6FB')

kpis = [
    ('Total Fund\nManagers',     str(len(dataset)),                                         '#003399'),
    ('Countries\nCovered',       str(dataset['country_primary'].nunique()),                  '#0066CC'),
    ('Total EIF\nCapital',       f"EUR {dataset['eif_commitment_eur'].sum()/1e6:.1f}M",     '#3399FF'),
    ('Funds Fit\nSolar',         str(int(dataset['solar_fit'].sum())),                       '#FFD700'),
    ('Funds Fit\nHydrogen',      str(int(dataset['hydrogen_fit'].sum())),                    '#FF6600'),
    ('Funds Fit\nDesalination',  str(int(dataset['desalination_fit'].sum())),                '#0099CC'),
]

for ax, (label, value, color) in zip(axes.flat, kpis):
    ax.set_facecolor(color)
    ax.text(0.5, 0.58, value, ha='center', va='center',
            fontsize=28, fontweight='bold', color='white', transform=ax.transAxes)
    ax.text(0.5, 0.2, label, ha='center', va='center',
            fontsize=11, color='white', alpha=0.9, transform=ax.transAxes)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

plt.suptitle('EU Funding Intelligence — EIF Fund Managers Overview',
             fontsize=14, fontweight='bold', color='#003399', y=1.02)
plt.tight_layout()
plt.show()
