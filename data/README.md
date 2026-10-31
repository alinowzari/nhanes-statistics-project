# Data Provenance and Reconstruction Guide (`data/`)

## 1. Official Data Source
All datasets used in this study originate from the **National Health and Nutrition Examination Survey (NHANES)**, August 2021–August 2023 Continuous Cycle, published by the **National Center for Health Statistics (NCHS)**, Centers for Disease Control and Prevention (CDC).

* **Official Portal:** [CDC NHANES 2021–2023 Continuous Data](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2021-2023)
* **Date Retrieved:** October 2026 (Aban 1405)
* **Access Level:** Public-Use Data Files (SAS Transport `.XPT` format)

---

## 2. Required Raw Files
In compliance with course guidelines, large raw `.XPT` files are excluded from version control via `.gitignore`. The three required files are:

| File Name | Module | Direct CDC URL | Raw Rows |
| :--- | :--- | :--- | :---: |
| `DEMO_L.XPT` | Demographics & Sample Weights | `https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/DEMO_L.XPT` | 11,933 |
| `BMX_L.XPT` | Body Measures (MEC) | `https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BMX_L.XPT` | 8,860 |
| `BPXO_L.XPT` | Oscillometric Blood Pressure (MEC) | `https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2021/DataFiles/BPXO_L.XPT` | 7,801 |

---

## 3. Automated Download and Cohort Reconstruction
To download the raw files into this `data/` directory and reconstruct the exact analytical cohort ($N = 5,805$), run from the repository root:

```bash
python src/download_data.py
python src/phase1_analysis.py