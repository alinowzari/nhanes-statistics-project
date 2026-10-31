import os
import warnings
import numpy as np
import pandas as pd
from scipy.stats import skew
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")

# -------------------------------------------------------------------------
# 0. DIRECTORY SETUP
# -------------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
FIG_DIR = os.path.join(BASE_DIR, "figures")
REPORT_DIR = os.path.join(BASE_DIR, "reports", "phase1")

os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# -------------------------------------------------------------------------
# 1. LOAD RAW DATA & MERGE ON SEQN (Tasks 1, 2, A1, A4)
# -------------------------------------------------------------------------
print("Loading NHANES 2021-2023 SAS Transport (.XPT) files...")
demo_raw = pd.read_sas(os.path.join(DATA_DIR, "DEMO_L.XPT"))
bmx_raw = pd.read_sas(os.path.join(DATA_DIR, "BMX_L.XPT"))
bpxo_raw = pd.read_sas(os.path.join(DATA_DIR, "BPXO_L.XPT"))

demo_cols = ["SEQN", "RIDAGEYR", "RIAGENDR", "WTINT2YR", "WTMEC2YR"]
bmx_cols = ["SEQN", "BMXBMI", "BMXWAIST"]
bpxo_cols = ["SEQN", "BPXOSY1", "BPXODI1"]

demo = demo_raw[demo_cols].copy()
bmx = bmx_raw[bmx_cols].copy()
bpxo = bpxo_raw[bpxo_cols].copy()

n_demo = len(demo)
n_bmx = len(bmx)
n_bpxo = len(bpxo)

# Deterministic 1-to-1 inner join on SEQN
merged = demo.merge(bmx, on="SEQN", how="inner").merge(bpxo, on="SEQN", how="inner")
n_merged = len(merged)

# Filter to adult population (Age >= 20 years)
adults = merged[merged["RIDAGEYR"] >= 20].copy()
n_adults = len(adults)

# -------------------------------------------------------------------------
# 2. DATA QUALITY AUDIT (Task 5)
# -------------------------------------------------------------------------
dup_seqn = adults["SEQN"].duplicated().sum()
missing_bmi = adults["BMXBMI"].isna().sum()
missing_sbp = adults["BPXOSY1"].isna().sum()
missing_dbp = adults["BPXODI1"].isna().sum()
zero_or_na_wt = (adults["WTMEC2YR"].isna() | (adults["WTMEC2YR"] <= 0)).sum()

# Construct final clean cohort (complete BMI, SBP, and strictly positive MEC weight)
df = adults.dropna(subset=["BMXBMI", "BPXOSY1", "WTMEC2YR"]).copy()
df = df[df["WTMEC2YR"] > 0].copy()
n_final = len(df)

# Check physiological plausibility & logical consistency in final cohort
implausible_bmi = ((df["BMXBMI"] < 10) | (df["BMXBMI"] > 100)).sum()
implausible_sbp = ((df["BPXOSY1"] < 50) | (df["BPXOSY1"] > 300)).sum()
valid_bp_pairs = df.dropna(subset=["BPXODI1"])
logical_bp_error = (valid_bp_pairs["BPXOSY1"] <= valid_bp_pairs["BPXODI1"]).sum()

def count_tukey_outliers(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    inner_low, inner_high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outer_low, outer_high = q1 - 3.0 * iqr, q3 + 3.0 * iqr
    mild = ((series < inner_low) | (series > inner_high)).sum()
    extreme = ((series < outer_low) | (series > outer_high)).sum()
    return inner_low, inner_high, mild, extreme

bmi_low, bmi_high, bmi_mild_out, bmi_ext_out = count_tukey_outliers(df["BMXBMI"])
sbp_low, sbp_high, sbp_mild_out, sbp_ext_out = count_tukey_outliers(df["BPXOSY1"])

# -------------------------------------------------------------------------
# 3. DERIVED CATEGORICAL VARIABLES & FREQUENCY TABLES (Tasks 4 & 6)
# -------------------------------------------------------------------------
df["Sex"] = df["RIAGENDR"].map({1.0: "Male", 2.0: "Female"})

df["Age_Group"] = pd.cut(
    df["RIDAGEYR"],
    bins=[19, 39, 59, np.inf],
    labels=["20-39 (Young Adult)", "40-59 (Middle-Aged)", "60+ (Older Adult)"],
    right=True,
)

df["BMI_Category"] = pd.cut(
    df["BMXBMI"],
    bins=[0, 18.5, 24.999, 29.999, np.inf],
    labels=[
        "Underweight (<18.5)",
        "Normal (18.5-24.9)",
        "Overweight (25.0-29.9)",
        "Obese (>=30.0)",
    ],
)

df["BP_Category"] = pd.cut(
    df["BPXOSY1"],
    bins=[0, 119.999, 129.999, 139.999, np.inf],
    labels=[
        "Normal (<120)",
        "Elevated (120-129)",
        "Stage 1 HTN (130-139)",
        "Stage 2 HTN (>=140)",
    ],
)

def build_frequency_table(dataframe, col_name):
    counts = dataframe[col_name].value_counts(sort=False)
    unweighted_pct = dataframe[col_name].value_counts(normalize=True, sort=False) * 100
    total_w = dataframe["WTMEC2YR"].sum()
    weighted_pct = (
        dataframe.groupby(col_name, observed=False)["WTMEC2YR"].sum() / total_w * 100
    )
    return pd.DataFrame({
        "Category": counts.index.astype(str),
        "Count (n)": counts.values,
        "Unweighted (%)": unweighted_pct.values.round(2),
        "Weighted (%)": weighted_pct.values.round(2),
    })

freq_sex = build_frequency_table(df, "Sex")
freq_age = build_frequency_table(df, "Age_Group")
freq_bmi = build_frequency_table(df, "BMI_Category")
freq_bp = build_frequency_table(df, "BP_Category")

# -------------------------------------------------------------------------
# 4. PARAMETRIC & NON-PARAMETRIC SUMMARY METRICS (Tasks 6 & 7)
# -------------------------------------------------------------------------
def summarize_continuous(series, label):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return {
        "Variable": label,
        "n": len(series),
        "Mean": round(series.mean(), 2),
        "SD": round(series.std(ddof=1), 2),
        "Median": round(series.median(), 2),
        "Q1 (25th)": round(q1, 2),
        "Q3 (75th)": round(q3, 2),
        "IQR": round(iqr, 2),
        "Min": round(series.min(), 2),
        "P5": round(series.quantile(0.05), 2),
        "P95": round(series.quantile(0.95), 2),
        "Max": round(series.max(), 2),
        "Skewness (g1)": round(skew(series, bias=False), 3),
    }

cont_summary = pd.DataFrame([
    summarize_continuous(df["BMXBMI"], "BMI (kg/m^2)"),
    summarize_continuous(df["BPXOSY1"], "Systolic BP (mmHg)"),
    summarize_continuous(df["RIDAGEYR"], "Age (Years)"),
])

# -------------------------------------------------------------------------
# 5. UNWEIGHTED VS. SURVEY-WEIGHTED ESTIMATORS (Tasks A2 & A3)
# -------------------------------------------------------------------------
def weighted_mean(x, w):
    return np.sum(x * w) / np.sum(w)

def weighted_sd(x, w):
    w_mean = weighted_mean(x, w)
    variance = np.sum(w * (x - w_mean) ** 2) / np.sum(w)
    return np.sqrt(variance)

def weighted_prop(cond, w):
    return (np.sum(cond * w) / np.sum(w)) * 100.0

w_vec = df["WTMEC2YR"]

weight_comparison = pd.DataFrame([
    {
        "Parameter / Indicator": "Mean BMI (kg/m^2)",
        "Unweighted": round(df["BMXBMI"].mean(), 2),
        "Weighted (WTMEC2YR)": round(weighted_mean(df["BMXBMI"], w_vec), 2),
    },
    {
        "Parameter / Indicator": "SD of BMI (kg/m^2)",
        "Unweighted": round(df["BMXBMI"].std(ddof=1), 2),
        "Weighted (WTMEC2YR)": round(weighted_sd(df["BMXBMI"], w_vec), 2),
    },
    {
        "Parameter / Indicator": "Mean Systolic BP (mmHg)",
        "Unweighted": round(df["BPXOSY1"].mean(), 2),
        "Weighted (WTMEC2YR)": round(weighted_mean(df["BPXOSY1"], w_vec), 2),
    },
    {
        "Parameter / Indicator": "SD of Systolic BP (mmHg)",
        "Unweighted": round(df["BPXOSY1"].std(ddof=1), 2),
        "Weighted (WTMEC2YR)": round(weighted_sd(df["BPXOSY1"], w_vec), 2),
    },
    {
        "Parameter / Indicator": "Mean Age (Years)",
        "Unweighted": round(df["RIDAGEYR"].mean(), 2),
        "Weighted (WTMEC2YR)": round(weighted_mean(df["RIDAGEYR"], w_vec), 2),
    },
    {
        "Parameter / Indicator": "Obesity Prevalence (BMI >= 30, %)",
        "Unweighted": round((df["BMXBMI"] >= 30).mean() * 100, 2),
        "Weighted (WTMEC2YR)": round(weighted_prop(df["BMXBMI"] >= 30, w_vec), 2),
    },
    {
        "Parameter / Indicator": "Elevated SBP Prevalence (SBP >= 130, %)",
        "Unweighted": round((df["BPXOSY1"] >= 130).mean() * 100, 2),
        "Weighted (WTMEC2YR)": round(weighted_prop(df["BPXOSY1"] >= 130, w_vec), 2),
    },
])
weight_comparison["Difference (Weighted - Raw)"] = (
    weight_comparison["Weighted (WTMEC2YR)"] - weight_comparison["Unweighted"]
).round(2)

# -------------------------------------------------------------------------
# 6. DESCRIPTIVE BIVARIATE GROUP COMPARISONS (Task 9)
# -------------------------------------------------------------------------
def subgroup_summary(dataframe, group_cols, target_col):
    rows = []
    for keys, sub in dataframe.groupby(group_cols, observed=False):
        if len(sub) == 0:
            continue
        key_label = " | ".join(str(k) for k in (keys if isinstance(keys, tuple) else (keys,)))
        q1 = sub[target_col].quantile(0.25)
        q3 = sub[target_col].quantile(0.75)
        rows.append({
            "Subgroup": key_label,
            "n": len(sub),
            "Mean": round(sub[target_col].mean(), 2),
            "SD": round(sub[target_col].std(ddof=1), 2),
            "Median": round(sub[target_col].median(), 2),
            "IQR": round(q3 - q1, 2),
            "Weighted Mean": round(weighted_mean(sub[target_col], sub["WTMEC2YR"]), 2),
        })
    return pd.DataFrame(rows)

sbp_by_bmi_sex = subgroup_summary(df, ["BMI_Category", "Sex"], "BPXOSY1")
sbp_by_age_sex = subgroup_summary(df, ["Age_Group", "Sex"], "BPXOSY1")
bmi_by_age_sex = subgroup_summary(df, ["Age_Group", "Sex"], "BMXBMI")

# -------------------------------------------------------------------------
# 7. PRINT & EXPORT COMPLETE STATISTICAL LEDGER
# -------------------------------------------------------------------------
output_lines = []
def log(text=""):
    print(text)
    output_lines.append(text)

log("=" * 75)
log("NHANES 2021-2023 PHASE 1 STATISTICAL OUTPUT LEDGER")
log("=" * 75)

log("\n[1] SAMPLE ATTRITION FLOW (Tasks A1 & A4)")
log(f"  DEMO_L raw count:                     {n_demo:,}")
log(f"  BMX_L raw count:                      {n_bmx:,}")
log(f"  BPXO_L raw count:                     {n_bpxo:,}")
log(f"  Merged intersection on SEQN:          {n_merged:,}")
log(f"  Excluded Age < 20 years:              {n_merged - n_adults:,}")
log(f"  Adult Cohort (Age >= 20):             {n_adults:,}")
log(f"  Excluded missing BMI/SBP/Weight:      {n_adults - n_final:,}")
log(f"  Final Analytical Sample (N):          {n_final:,}")

log("\n[2] DATA QUALITY & OUTLIER AUDIT (Task 5)")
log(f"  Duplicate SEQN IDs in adult cohort:   {dup_seqn}")
log(f"  Missing BMXBMI in adult cohort:       {missing_bmi}")
log(f"  Missing BPXOSY1 in adult cohort:      {missing_sbp}")
log(f"  Missing/Zero WTMEC2YR in adults:      {zero_or_na_wt}")
log(f"  Implausible BMI (<10 or >100):        {implausible_bmi}")
log(f"  Implausible SBP (<50 or >300):        {implausible_sbp}")
log(f"  Logical violations (SBP <= DBP):      {logical_bp_error}")
log(f"  BMI Tukey 1.5*IQR fences:             [{bmi_low:.2f}, {bmi_high:.2f}] -> {bmi_mild_out} outside ({bmi_ext_out} > 3*IQR)")
log(f"  SBP Tukey 1.5*IQR fences:             [{sbp_low:.2f}, {sbp_high:.2f}] -> {sbp_mild_out} outside ({sbp_ext_out} > 3*IQR)")

log("\n[3] CATEGORICAL FREQUENCY TABLES (Task 6)")
log("--- Biological Sex ---")
log(freq_sex.to_string(index=False))
log("\n--- Age Cohort ---")
log(freq_age.to_string(index=False))
log("\n--- Clinical BMI Category ---")
log(freq_bmi.to_string(index=False))
log("\n--- Systolic BP Category ---")
log(freq_bp.to_string(index=False))

log("\n[4] PARAMETRIC & NON-PARAMETRIC SUMMARY METRICS (Tasks 6 & 7)")
log(cont_summary.to_string(index=False))

log("\n[5] UNWEIGHTED VS. SURVEY-WEIGHTED COMPARISON (Tasks A2 & A3)")
log(weight_comparison.to_string(index=False))

log("\n[6] DESCRIPTIVE BIVARIATE COMPARISONS (Task 9)")
log("--- Systolic BP (mmHg) by BMI Category & Sex ---")
log(sbp_by_bmi_sex.to_string(index=False))
log("\n--- Systolic BP (mmHg) by Age Group & Sex ---")
log(sbp_by_age_sex.to_string(index=False))
log("\n--- BMI (kg/m^2) by Age Group & Sex ---")
log(bmi_by_age_sex.to_string(index=False))

ledger_path = os.path.join(REPORT_DIR, "computed_metrics.txt")
with open(ledger_path, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))
print(f"\n[SAVED] Complete statistical ledger written to: {ledger_path}")

# -------------------------------------------------------------------------
# 8. GENERATE 4 PUBLICATION-QUALITY FIGURES (Tasks 8 & 9)
# -------------------------------------------------------------------------
sns.set_theme(style="whitegrid", font_scale=1.05)

# Figure 1: Empirical Distribution of BMI (Histogram + KDE + Center Lines)
plt.figure(figsize=(8.5, 5.2))
sns.histplot(df["BMXBMI"], kde=True, bins=42, color="#1f77b4", edgecolor="white", alpha=0.75)
plt.axvline(df["BMXBMI"].mean(), color="#d62728", linestyle="--", linewidth=2, label=f"Mean = {df['BMXBMI'].mean():.2f} kg/m²")
plt.axvline(df["BMXBMI"].median(), color="#2ca02c", linestyle="-", linewidth=2, label=f"Median = {df['BMXBMI'].median():.2f} kg/m²")
plt.title("Figure 1: Empirical Distribution of Body Mass Index in US Adults (N = 5,805)", fontsize=12.5, weight="bold")
plt.xlabel("Body Mass Index (kg/m²)")
plt.ylabel("Participant Count (Frequency)")
plt.legend(frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig1_bmi_distribution.png"), dpi=300)
plt.close()

# Figure 2: Empirical Distribution of Systolic Blood Pressure
plt.figure(figsize=(8.5, 5.2))
sns.histplot(df["BPXOSY1"], kde=True, bins=42, color="#ff7f0e", edgecolor="white", alpha=0.75)
plt.axvline(df["BPXOSY1"].mean(), color="#d62728", linestyle="--", linewidth=2, label=f"Mean = {df['BPXOSY1'].mean():.2f} mmHg")
plt.axvline(df["BPXOSY1"].median(), color="#2ca02c", linestyle="-", linewidth=2, label=f"Median = {df['BPXOSY1'].median():.2f} mmHg")
plt.title("Figure 2: Empirical Distribution of First Systolic Blood Pressure Reading (N = 5,805)", fontsize=12.5, weight="bold")
plt.xlabel("Systolic Blood Pressure (mmHg)")
plt.ylabel("Participant Count (Frequency)")
plt.legend(frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig2_sbp_distribution.png"), dpi=300)
plt.close()

# Figure 3: Demographic Structure across Age Groups and Biological Sex
plt.figure(figsize=(8.5, 5.2))
ax = sns.countplot(data=df, x="Age_Group", hue="Sex", palette=["#2b5c8f", "#d95f02"])
plt.title("Figure 3: Analytical Cohort Distribution by Age Bracket and Biological Sex (N = 5,805)", fontsize=12.5, weight="bold")
plt.xlabel("Adult Age Cohort (Years)")
plt.ylabel("Number of Participants (n)")
plt.legend(title="Biological Sex", frameon=True)
for p in ax.patches:
    height = p.get_height()
    if height > 0:
        ax.annotate(
            f"{int(height):,}",
            (p.get_x() + p.get_width() / 2.0, height),
            ha="center",
            va="bottom",
            fontsize=9.5,
            xytext=(0, 3),
            textcoords="offset points",
        )
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig3_demographics.png"), dpi=300)
plt.close()

# Figure 4: Bivariate Descriptive Comparison of SBP across BMI Categories & Sex
plt.figure(figsize=(9.2, 5.4))
sns.boxplot(
    data=df,
    x="BMI_Category",
    y="BPXOSY1",
    hue="Sex",
    palette=["#2b5c8f", "#d95f02"],
    fliersize=3,
)
plt.title("Figure 4: Systolic Blood Pressure Stratified by Clinical BMI Tier and Sex (N = 5,805)", fontsize=12.5, weight="bold")
plt.xlabel("Clinical Body Mass Index Category (kg/m²)")
plt.ylabel("Systolic Blood Pressure (mmHg)")
plt.legend(title="Biological Sex", frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, "fig4_bivariate_comparison.png"), dpi=300)
plt.close()

print(f"[SAVED] All 4 publication-grade figures saved in: {FIG_DIR}")