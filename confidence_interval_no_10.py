import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
 
# DATA HANDLING -------------------

UTS_vals = [
    73.8, 75.2, 75.6, 69.0, 70.6,
    38.0, 37.8, 36.2, 
    42.1, 37.8, 44.8, 
    49.6, 55.9, 54.0, 
]
diameters = [
    6, 6, 6, 6, 6,
    16, 16, 16,
    12, 12, 12,
    8, 8, 8,
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

def scipy_fit(x, y):
    x = np.array(x)
    y = np.array(y)

    def model(x, a, b, c):
        return a + b/(x-c)

    initial_guess = [1, 1000, 1]

    params, covariance = curve_fit(model, x, y, p0=initial_guess)
    a, b, c = params
    v = covariance

    x_vals = np.linspace(min(x), max(x), 100)
    y_vals = model(x_vals, a, b, c)

    rmse = np.sqrt(np.sum((model(x, a,b,c) - y)**2)/len(y))

    return x_vals, y_vals, a, b, c, rmse, v, params


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
plt.figure(figsize=(12, 6))

plt.scatter(dias, uts, s=50, alpha=0.7, label='Data')

x, y, a,b,c,rmse,v, popt= scipy_fit(dias, uts)

def model(x, a, b, c):
        return a + b/(x-c)

def confidence_interval(x, popt, v):
    sig_y = []
    
    for xi in x:
        e = 1e-8
        jac = []
        for i in range(len(popt)):
            p0 = np.copy(popt)
            p1 = np.copy(popt)
            p0[i] -= e
            p1[i] += e
            grad = (model(xi, *p1) - model(xi, *p0)) / (2 * e)
            jac.append(grad)
        
        jac = np.array(jac)
        
        var_y = np.dot(jac.T, np.dot(v, jac))
        sig_y.append(np.sqrt(var_y))
        
    return np.array(sig_y)

sigma_y = confidence_interval(x, popt, v)
ci_95 = 1.96 * sigma_y

plt.plot(x, y, alpha=0.7, color="#F07408",
         linewidth=2.5, label=f'Best Fit of form Y = A + B/(X - C)\nA = {a:.3f}\nB = {b:.3f}\nC = {c:.3f}\nRMS Error = {rmse:.4f}')
plt.fill_between(x, y - ci_95, y + ci_95, color='red', alpha=0.2, label='95% Confidence Interval')
plt.title("UTS vs Diameter", weight='bold')
plt.xlabel("Diameter (mm)")
plt.ylabel("Average UTS (MPa)")

plt.legend(frameon=True)
plt.tight_layout()
plt.show()