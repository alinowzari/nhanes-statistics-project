# Project Card: NHANES 2021–2023 Analysis

## 1. Dataset and Cycle
* **Source:** CDC / NCHS Continuous NHANES 2021–August 2023 public-use files.
* **Component Files:**
  * `DEMO_L.XPT`: Demographics and Survey Design Weights (`WTMEC2YR`).
  * `BMX_L.XPT`: Body Measures Examination Data (`BMXBMI`).
  * `BPXO_L.XPT`: Oscillometric Blood Pressure Examination Data (`BPXOSY1`).

## 2. Working Title
* An Empirical Investigation of Body Mass Index, Blood Pressure, and Demographic Disparities in Non-Institutionalized US Adults (NHANES 2021–2023).

## 3. Primary Statistical Question
* How do empirical distributions of Body Mass Index (BMI) and Systolic Blood Pressure (SBP) vary across age tiers and biological sex in civilian non-institutionalized US adults, and what is the observational relationship between elevated BMI and SBP?

## 4. Unit of Observation and Target Population
* **Unit of Observation:** A single human participant uniquely identified by sequence number (`SEQN`).
* **Analyzed Sample Size:** $N = 5{,}805$ adult respondents with complete MEC examination data.
* **Interpretable Target Population:** Civilian, non-institutionalized US adult population aged 20 years and older.

## 5. Key Variables and Measurement Scales
* `SEQN`: Unique respondent identification key (Qualitative, Nominal).
* `RIAGENDR`: Biological sex (Qualitative, Nominal: 1 = Male, 2 = Female).
* `RIDAGEYR`: Age in years at screening (Quantitative, Discrete).
* `BMXBMI`: Body Mass Index in $\text{kg/m}^2$ (Quantitative, Continuous ratio scale).
* `BPXOSY1`: First oscillometric systolic blood pressure in $\text{mmHg}$ (Quantitative, Continuous ratio scale).
* `WTMEC2YR`: Full sample 2-year Mobile Examination Center exam weight (Continuous probability calibration factor).

## 6. Role of Variables
* **Primary Quantitative Responses / Outcomes:** `BMXBMI` and `BPXOSY1`.
* **Explanatory / Stratification Factors:** `RIDAGEYR` (partitioned into 20–39, 40–59, and 60+ cohorts) and `RIAGENDR`.

## 7. Question Classification
* Descriptive, comparative, and observational associative (strictly non-causal).

## 8. Initial Scientific Hypothesis
* Median systolic blood pressure increases across progressive BMI tiers, with observable upward shifts across older age cohorts.

## 9. Initial Foreseeable Limitations
* **Observational Design:** Cross-sectional data prevents establishing temporal sequence or causal mechanisms.
* **Selection / Non-Response Bias:** 259 examination participants were dropped due to missing physiological records or zero exam weights, which may slightly alter sample composition.