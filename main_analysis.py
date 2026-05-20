"""
=============================================================================
Volume–effectiveness analysis of CSO storage based on SWMM
Data Analysis and Visualization Script
=============================================================================
This script performs the statistical curve-fitting and visualizes the 
aggregated data presented in the manuscript. Due to non-disclosure agreements 
(NDAs) regarding critical municipal infrastructure, raw SWMM .inp files are 
omitted. This script utilizes the de-identified, aggregated simulation results.
=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score
import os

# Set global plot style for publication
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'font.size': 12, 'font.family': 'serif'})

# Create output directory for figures
os.makedirs('figures', exist_ok=True)

def plot_fig13_polynomial_regression():
    """
    Performs localized polynomial regression (active reversal zone 7-30 mm)
    to statistically identify the critical rainfall depth breakpoint (Fig 13).
    """
    print("--- Running Analysis for Fig 13: Polynomial Regression ---")
    df = pd.read_csv('data/fig12_ncr_data.csv', index_col='volume')
    
    # Extract baseline data (0m3)
    rainfall_depths = np.array([0, 2, 5, 7, 10, 15, 20, 30, 50])
    ncr_baseline = df.loc['0m³'].values
    
    # Isolate the active reversal zone (7 mm to 30 mm) for localized fitting
    mask = (rainfall_depths >= 7) & (rainfall_depths <= 30)
    x_sub = rainfall_depths[mask]
    y_sub = ncr_baseline[mask]
    
    # Fit a 2nd-degree polynomial: y = c0 + c1*x + c2*x^2
    coeffs = np.polyfit(x_sub, y_sub, 2)
    poly_func = np.poly1d(coeffs)
    
    # Calculate R-squared
    y_pred = poly_func(x_sub)
    r2 = r2_score(y_sub, y_pred)
    
    # Calculate analytical peak (vertex of parabola): x = -c1 / (2*c2)
    peak_x = -coeffs[1] / (2 * coeffs[0])
    peak_y = poly_func(peak_x)
    
    print(f"Polynomial Coefficients: {coeffs}")
    print(f"R-squared: {r2:.3f}")
    print(f"Identified Statistical Breakpoint: {peak_x:.2f} mm")
    
    # Plotting
    plt.figure(figsize=(8, 6))
    plt.plot(rainfall_depths, ncr_baseline, 'ko', label='Observed NCR Data ($0 m^3$ baseline)')
    
    # Generate smooth curve for the fit
    x_smooth = np.linspace(7, 30, 100)
    y_smooth = poly_func(x_smooth)
    plt.plot(x_smooth, y_smooth, 'r-', linewidth=2, label=f'Localized Polynomial Fit ($R^2={r2:.3f}$)')
    
    # Highlight the peak
    plt.axvline(x=peak_x, color='blue', linestyle='--', alpha=0.7)
    plt.plot(peak_x, peak_y, 'bo', markersize=8)
    plt.annotate(f'Statistical Threshold:\n{peak_x:.1f} mm', 
                 xy=(peak_x, peak_y), xytext=(peak_x, peak_y + 5),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6),
                 horizontalalignment='center', color='blue', fontweight='bold')
    
    plt.xlabel('Accumulated Rainfall Depth (mm)')
    plt.ylabel('COD Non-Compliance Rate (NCR, %)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('figures/Fig13_Polynomial_Fit.png', dpi=300)
    plt.close()


def plot_fig16_sensitivity():
    """
    Visualizes the One-At-a-Time (OAT) Sensitivity Analysis (Fig 16).
    """
    print("--- Generating Fig 16: Sensitivity Analysis ---")
    df = pd.read_csv('data/fig16_sensitivity.csv')
    
    # Create labels like "n_imperv (-20%)"
    df['Label'] = df['item'] + ' (' + df['value'].astype(str) + '%)'
    
    # Setup plot
    fig, ax = plt.subplots(figsize=(10, 8))
    y_pos = np.arange(len(df['Label']))
    height = 0.35
    
    ax.barh(y_pos - height/2, df['volume_sensitivity'], height, label='Overflow Volume Sensitivity (%)', color='steelblue')
    ax.barh(y_pos + height/2, df['cod_mass_sensitivity'], height, label='COD Mass Load Sensitivity (%)', color='firebrick')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df['Label'])
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('OAT Parameter Sensitivity Coefficient (%)')
    ax.set_title('Sensitivity of Overflow Volume and COD Mass to Parameter Perturbations', fontweight='bold')
    ax.legend(loc='lower right')
    
    plt.tight_layout()
    plt.savefig('figures/Fig16_Sensitivity_Analysis.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    print("Starting data analysis pipeline...")
    plot_fig13_polynomial_regression()
    plot_fig16_sensitivity()
    print("Analysis complete. Figures saved in 'figures/' directory.")