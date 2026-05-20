# Volume–Effectiveness Analysis of CSO Storage Based on SWMM

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

This repository contains the analytical source code and aggregated datasets for the manuscript: **"Volume–effectiveness analysis of CSO storage based on SWMM: a case study in Jiujiang"**.

## 📌 Data Availability & Confidentiality Statement
Due to strict Non-Disclosure Agreements (NDAs) mandated by local utility authorities regarding critical municipal infrastructure, the foundational high-resolution SWMM input files (`.inp`) and detailed underground drainage network topologies cannot be made publicly available. 

However, to ensure **complete methodological transparency and computational reproducibility**, we provide the de-identified, aggregated model outputs used for the statistical analyses and optimizations discussed in the manuscript. Vetted academic researchers may request access to anonymized portions of the raw structural data by contacting the corresponding author, subject to approval and specific data-sharing agreements.

## 📂 Repository Structure
- `data/`: Contains the aggregated simulation output files.
  - `fig11_reduction_rate.csv`: COD load reduction rates across different rainfall depths and storage volumes for the top 4 critical outlets.
  - `fig12_ncr_data.csv`: Riverine Non-Compliance Rate (NCR) variations.
  - `fig16_sensitivity.csv`: Data for the One-At-a-Time (OAT) parameter sensitivity analysis.
- `main_analysis.py`: The core Python script that performs mathematical curve-fitting (e.g., the localized polynomial regression for breakpoint identification) and generates the figures.
- `requirements.txt`: Python dependencies.

## 🚀 How to Run the Code
1. Ensure Python 3.8+ is installed.
2. Install the required packages:
   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn
3. Execute the analysis script:
   ```bash
   python main_analysis.py
```bash
### 📊 Key Statistical Highlights in the Code

**Fig 13 Breakpoint Analysis:** The script rigorously applies a 2nd-degree localized polynomial regression strictly within the active hydrologic reversal zone (7-30 mm). By calculating the mathematical vertex of the fitted parabola ($X_{peak} = -c_1 / 2c_2$), it exacts the threshold at 18.0 mm ($R^2 = 0.989$), statistically validating the volumetric dilution effect.
```
