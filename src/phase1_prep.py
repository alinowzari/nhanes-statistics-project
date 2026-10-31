import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

print("Reading raw XPT files...")
demo_raw = pd.read_sas(os.path.join(DATA_DIR, "DEMO_L.XPT"))
bmx_raw = pd.read_sas(os.path.join(DATA_DIR, "BMX_L.XPT"))
bpxo_raw = pd.read_sas(os.path.join(DATA_DIR, "BPXO_L.XPT"))

# Extract target columns
demo = demo_raw[["SEQN", "RIDAGEYR", "RIAGENDR", "WTMEC2YR"]].copy()
bmx = bmx_raw[["SEQN", "BMXBMI"]].copy()
bpxo = bpxo_raw[["SEQN", "BPXOSY1"]].copy()

n_demo = len(demo)
n_bmx = len(bmx)
n_bpxo = len(bpxo)

# 1. Merge on SEQN
merged = demo.merge(bmx, on="SEQN", how="inner")
merged = merged.merge(bpxo, on="SEQN", how="inner")
n_merged = len(merged)

# 2. Filter Adults (Age >= 20)
adults = merged[merged["RIDAGEYR"] >= 20].copy()
n_adults = len(adults)

# 3. Drop missing/invalid values
clean_cohort = adults.dropna(
    subset=["BMXBMI", "BPXOSY1", "WTMEC2YR"]
).copy()
clean_cohort = clean_cohort[clean_cohort["WTMEC2YR"] > 0]
n_final = len(clean_cohort)

print("\n" + "=" * 55)
print("            SAMPLE ATTRITION FLOW TABLE")
print("=" * 55)
print(f"1. Demographics raw participants (DEMO_L):     {n_demo:,}")
print(f"2. Body measures raw participants (BMX_L):      {n_bmx:,}")
print(f"3. Blood pressure raw participants (BPXO_L):    {n_bpxo:,}")
print("-" * 55)
print(f"4. Merged participants (SEQN intersection):     {n_merged:,}")
print(f"5. Excluded adolescents/pediatrics (Age < 20):  {n_merged - n_adults:,}")
print(f"6. Adult cohort (Age >= 20):                    {n_adults:,}")
print(f"7. Excluded missing BMI, SBP, or zero weight:   {n_adults - n_final:,}")
print("-" * 55)
print(f"8. Final analytical sample size (N):            {n_final:,}")
print("=" * 55)