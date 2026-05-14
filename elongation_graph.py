import numpy as np
import matplotlib.pyplot as plt

BASE_PATH = "Graphs"


# DATA HANDLING -------------------

diameters = [
    6, 6, 6, 6, 6,
    16, 16, 16,
    12, 12, 12,
    8, 8, 8, 8, 8,
    10, 10, 10, 10 #extra 10 only for this graph, don't copy paste these into others
]


# PLOTTING-------------

plt.style.use('seaborn-v0_8-whitegrid')  # clean modern style

plt.rcParams.update({
    'font.size': 14,          # base size
    'axes.titlesize': 18,     # title
    'axes.labelsize': 16,     # x/y labels
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 14     # legend text
})

# ---- Plot 1: UTS vs Diameter ----
plt.figure(figsize=(8, 5))


lis = [
    7.3, 11.1, 14.8, 15, 19.9,
    3.2, 3.9, 3.9,
    4.8, 5, 7.5,
    4.5, 5.4, 5.6, 4.2, 4.8, 
    7.3, 8.1, 8.9, 10

]

plt.scatter(diameters, lis, s=50, alpha=0.7)
# plt.plot(plot_dias, avg_uts, color="#F07408", alpha=0.7, linewidth=2.5, label='Trend')

plt.title(fr"Elongation (% strain) at Break", weight='bold')
plt.xlabel("Diameter (mm)")
plt.ylabel("Elongation at breakage")

plt.legend()
plt.tight_layout()
plt.savefig(fname=f'{BASE_PATH}/elongation', dpi=600, bbox_inches='tight')
plt.show()
