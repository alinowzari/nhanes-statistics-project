# Project Card: NHANES 2021–2023 Analysis

* **Author:** Ali Nowzari
* **Student ID:** 403100292
* **Track:** Track A — CDC/NCHS National Health and Nutrition Examination Survey (NHANES 2021–2023)
* **Git Tag:** `phase-1`

---

## 1. Dataset and Cycle
* **Source:** CDC / NCHS Continuous NHANES August 2021–August 2023 public-use files.
* **Component Files:**
  * `DEMO_L.XPT`: Demographics and Survey Design Weights (`RIDAGEYR`, `RIAGENDR`, `WTINT2YR`, `WTMEC2YR`).
  * `BMX_L.XPT`: Body Measures Examination Data (`BMXBMI`, `BMXWAIST`).
  * `BPXO_L.XPT`: Oscillometric Blood Pressure Examination Data (`BPXOSY1`, `BPXODI1`).

## 2. Working Title
* An Empirical Investigation of Body Mass Index, Systolic Blood Pressure, and Demographic Structure in US Adults (NHANES 2021–2023).

## 3. Primary Statistical Question
* Among civilian, non-institutionalized United States adults aged 20 years and older in NHANES 2021–2023 ($N = 5,805$), how do the empirical distributions of Body Mass Index (`BMXBMI`) and first oscillometric Systolic Blood Pressure (`BPXOSY1`) vary across adult age brackets and biological sex, how strongly is `BMXBMI` associated with `BPXOSY1` after accounting for age (`RIDAGEYR`) and biological sex (`RIAGENDR`), and how do complex survey sampling weights (`WTMEC2YR`) modify descriptive and inferential conclusions?

## 4. Unit of Observation and Target Population
* **Unit of Observation:** A single examined human participant uniquely identified by respondent sequence number (`SEQN`), maintaining a strict one-row-per-participant cross-sectional structure.
* **Analyzed Sample Size:** $N = 5,805$ adult respondents ($\text{Age} \ge 20$ years) with complete MEC body measure and blood pressure records and strictly positive examination weights (`WTMEC2YR > 0`).
* **Interpretable Target Population:** Civilian, non-institutionalized US adult population aged 20 years and older residing in the 50 states and the District of Columbia.

## 5. Key Variables and Measurement Scales
* `SEQN`: Unique respondent identification key (Qualitative, Nominal).
* `RIAGENDR`: Biological sex (Qualitative, Binary Nominal: `1 = Male`, `2 = Female`).
* `RIDAGEYR`: Age in years at screening, top-coded at 80 years (Quantitative, Discrete Ratio).
* `BMXBMI`: Body Mass Index in $\text{kg/m}^2$ (Quantitative, Continuous Ratio).
* `BPXOSY1`: First oscillometric systolic blood pressure reading in $\text{mmHg}$ (Quantitative, Continuous Ratio).
* `WTMEC2YR`: Full sample 2-year Mobile Examination Center weight (Quantitative, Continuous Ratio calibration factor).
* `Age_Group`: Derived adult age cohort (`20-39`, `40-59`, `60+` years; Qualitative, Ordinal).
* `BMI_Category`: Derived clinical BMI tier (`Underweight <18.5`, `Normal 18.5-24.9`, `Overweight 25.0-29.9`, `Obese >=30.0`; Qualitative, Ordinal).
* `BP_Category`: Derived systolic blood pressure tier (`Normal <120`, `Elevated 120-129`, `Stage 1 HTN 130-139`, `Stage 2 HTN >=140`; Qualitative, Ordinal).

## 6. Role of Variables
* **Primary Quantitative Response / Outcome:** `BPXOSY1` (Systolic Blood Pressure).
* **Primary Quantitative Explanatory Variable:** `BMXBMI` (Body Mass Index), analyzed univariately in Phase 1 and as the primary adiposity exposure predicting `BPXOSY1` in bivariate and regression analyses.
* **Demographic Explanatory / Stratification Factors:** `RIDAGEYR` (partitioned into `20–39`, `40–59`, and `60+` cohorts) and `RIAGENDR` (Biological Sex).
* **Survey Calibration Weight:** `WTMEC2YR` (accounts for unequal selection probabilities, MEC non-response, and post-stratification).

## 7. Question Classification
* Descriptive, comparative, and observational associative (strictly non-causal).

## 8. Initial Scientific Hypothesis
* Central systolic blood pressure (`BPXOSY1`) increases across progressive clinical BMI tiers (`BMXBMI`), with substantial upward shifts and wider dispersion across older age cohorts (`RIDAGEYR`) that partially confound unadjusted marginal BMI-SBP comparisons.

## 9. Initial Foreseeable Limitations
* **Observational Cross-Sectional Design:** Lack of temporal precedence and randomization prevents establishing causal mechanisms between adiposity and blood pressure.
* **Complete-Case Attrition:** Out of $6,064$ eligible adult MEC examinees, $259$ records ($4.27\%$) were excluded due to missing `BMXBMI` ($n = 94$) or `BPXOSY1` ($n = 201$; $36$ missing both).
* **Right-Censoring / Top-Coding of Age:** NCHS top-codes `RIDAGEYR` at 80 years for disclosure protection, truncating exact age variation among the oldest-old ($\ge 80$ years).