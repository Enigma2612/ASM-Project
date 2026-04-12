import numpy as np
import matplotlib.pyplot as plt

BASE_PATH = "Graphs"



# DATA HANDLING -------------------

UTS_vals = [
    73.8, 75.2, 75.6, 69.0, 70.6,
    38.0, 37.8, 36.2, 42.1, 37.8,
    44.8, 49.6, 55.9, 54.0, 48.7,
    51.0, 62.6, 62.9, 63.8, 61.7
]
diameters = [
    6, 6, 6, 6, 6,
    16, 16, 16,
    12, 12, 12,
    8, 8, 8, 8, 8,
    10, 10, 10, 10
]

uts_vs_dia = list(zip(diameters, UTS_vals))
uts_vs_dia.sort()
print(uts_vs_dia)

dias, uts = list(zip(*uts_vs_dia))
areas = np.array(dias)**2 * np.pi / 4

dia_to_uts = {}

for d, u in uts_vs_dia:
    dia_to_uts[d] = dia_to_uts.get(d, []) + [u]

plot_dias = []
avg_uts = []

for d, u in dia_to_uts.items():
    plot_dias.append(d)
    avg_uts.append(sum(u)/len(u))

plot_areas = np.array(plot_dias)**2 * np.pi / 4

# FUNCTIONS-----------


def powerfit(x, y):
    coeffs = np.polyfit(np.log(x), np.log(y), 1)
    x_vals = np.linspace(np.log(min(x)), np.log(max(x)), 100)
    y_vals = np.polyval(coeffs, x_vals)

    x_vals = np.exp(x_vals)
    y_vals = np.exp(y_vals)
    return x_vals, y_vals

# PLOTTING-------------


plt.style.use('seaborn-v0_8-whitegrid')  # clean modern style

# ---- Plot 1: UTS vs Diameter ----
plt.figure(figsize=(8, 5))

plt.scatter(dias, uts, s=50, alpha=0.7, label='Data')
# plt.plot(plot_dias, avg_uts, color='orange', linewidth=2.5, label='Trend')

x, y = powerfit(plot_dias, avg_uts)

plt.plot(x, y, alpha=0.7, color="#F07408",
         linewidth=2.5, label='Power Law Fit')

plt.title("UTS vs Diameter", fontsize=14, weight='bold')
plt.xlabel("Diameter (mm)", fontsize=12)
plt.ylabel("UTS (MPa)", fontsize=12)

plt.legend()
plt.tight_layout()
plt.savefig(fname=f'{BASE_PATH}/uts_vs_dia_powerfit', dpi=600, bbox_inches='tight')
plt.show()


# ---- Plot 2: UTS vs Area ----
plt.figure(figsize=(8, 5))

plt.scatter(areas, uts, s=50, alpha=0.7, label='Data')
x, y = powerfit(plot_areas, avg_uts)
plt.plot(x, y, alpha=0.7, color="#5A09BC",
         linewidth=2.5, label='Power Law Fit')
plt.title("UTS vs Area", fontsize=14, weight='bold')
plt.xlabel("Area (mm²)", fontsize=12)
plt.ylabel("UTS (MPa)", fontsize=12)

plt.legend()
plt.tight_layout()
plt.savefig(f'{BASE_PATH}/uts_vs_area_powerfit', dpi=600, bbox_inches='tight')
plt.show()
