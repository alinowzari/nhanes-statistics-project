# Statistical Foundations to Reproducible Research — NHANES 2021–2023

* **Author:** Ali Nowzari
* **Student ID:** 403100292
* **Course:** Statistics (Fall 1405 / 2026)
* **Dataset Track:** Track A — CDC/NCHS National Health and Nutrition Examination Survey (NHANES August 2021–August 2023)

---

## Project Overview
This repository contains the reproducible code, statistical ledger, figures, and formal reports for a five-phase statistical investigation of **Body Mass Index (`BMXBMI`)**, **Systolic Blood Pressure (`BPXOSY1`)**, **Age (`RIDAGEYR`)**, and **Biological Sex (`RIAGENDR`)** among civilian, non-institutionalized United States adults ($N = 5,805$).

---

## Repository Structure
```text
nhanes-statistics-project/
├── PROJECT_CARD.md                 # Formal statistical framework and variable definitions
├── README.md                       # Project documentation and reproduction guide
├── requirements.txt                # Python package dependencies
├── data/
│   └── README.md                   # Data provenance, CDC URLs, and cohort reconstruction
├── src/
│   ├── download_data.py            # Automated script to fetch raw CDC .XPT files
│   └── phase1_analysis.py          # Phase 1 merging, quality audit, summaries, and plots
├── figures/
│   ├── fig1_bmi_distribution.png   # BMI histogram + KDE with Mean & Median
│   ├── fig2_sbp_distribution.png   # Systolic BP histogram + KDE with Mean & Median
│   ├── fig3_demographics.png       # Sample composition across age brackets and sex
│   └── fig4_bivariate_comparison.png # Stratified boxplots of SBP across BMI tiers & sex
└── reports/
    ├── phase1.pdf                  # Compiled Phase 1 Report (Root copy)
    └── phase1/
        ├── phase1.pdf              # Compiled Phase 1 Report
        ├── phase1.tex              # LaTeX source code
        └── computed_metrics.txt    # Complete Phase 1 statistical output ledger