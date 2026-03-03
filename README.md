# Data Lifecycle Management - Smart Agriculture

Repository: `data-lifecycle-smart-agriculture-23082010054`

---

## Overview

This project demonstrates a complete data lifecycle workflow applied to a smart agriculture dataset. The workflow covers data acquisition, pre-processing, exploratory analysis, visualization, and documentation of data quality governance.

**Workflow stages:**

| Stage | Tool / Method |
|---|---|
| Data acquisition | Kaggle dataset download |
| Processing and cleaning | Google Colab (Python) |
| Visualization and dashboard | Streamlit |
| Documentation and governance | Data quality metrics, screenshots, README |

---

## Dataset

- **Source:** Kaggle — [`chaitanyagopidesi/smart-agriculture-dataset`](https://www.kaggle.com/datasets/chaitanyagopidesi/smart-agriculture-dataset)
- **Raw data (original):** `data/raw/`
- **Cleaned data (output):** `outputs/cleaned_data.csv`

---

## Project Structure

```text
data-lifecycle-smart-agriculture-23082010054/
├── data/
│   └── raw/                        # Raw dataset (original, unchanged files)
├── outputs/
│   ├── cleaned_data.csv            # Cleaned dataset
│   └── data_quality_metrics.csv   # Data quality scores
├── dashboard/
│   └── app.py                      # Streamlit dashboard
├── docs/
│   └── screenshots/
│       ├── dashboard.png
│       ├── eda.png
│       └── analysis.png
├── requirements.txt                # Python dependencies
└── README.md
```

---

## Setup and Acquisition

1. Download the dataset from Kaggle:
   ```bash
   kaggle datasets download -d chaitanyagopidesi/smart-agriculture-dataset
   ```
2. Extract and place the raw files inside `data/raw/`.
3. Commit the raw data without any modification. Raw files must remain unchanged throughout the project.

---

## Processing and Analysis (Google Colab)

All cleaning and analysis steps are performed in Google Colab using Python (pandas, matplotlib, seaborn).

**Steps performed:**

1. **Exploratory Data Analysis (EDA)**
   - `describe()` for statistical summary
   - Missing values check
   - Target distribution analysis

2. **Data Cleaning**
   - Standardize column names (lowercase, underscores)
   - Remove duplicate rows
   - Outlier handling using IQR capping on all numeric columns

3. **Output**
   - Cleaned dataset saved to `outputs/cleaned_data.csv`
   - Data quality metrics saved to `outputs/data_quality_metrics.csv`

---

## Visualization and Dashboard (Streamlit)

**Dashboard location:** `dashboard/app.py`

**Visualizations included:**

| Visualization | Description |
|---|---|
| Trend chart (proxy) | Sensor averages grouped by `seedling_stage` (no timestamp column available) |
| Gauge | Current humidity level |
| Correlation heatmap | Relationship among sensor readings and yield target |
| Alert system | Triggered when humidity drops below a user-defined threshold |

**Run locally:**

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

**Deployment (Streamlit Community Cloud):**

- Main file path: `dashboard/app.py`
- Public URL: `PASTE_YOUR_STREAMLIT_PUBLIC_URL_HERE`

---

## Documentation and Governance

### Data Quality Metrics

Metrics are computed and stored in `outputs/data_quality_metrics.csv`.

**Definitions used in this assignment:**

| Metric | Formula |
|---|---|
| Accuracy | `1 - (missing_cells / total_cells)` |
| Completeness | `non_null_cells / total_cells` |
| Timeliness | Percentage of records within the last 30 days (requires a timestamp column) |

**Data Quality Results:**

| Dataset | Rows | Cols | Missing Cells | Total Cells | Accuracy | Completeness | Timeliness (30d) | Note |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| _Generate `outputs/data_quality_metrics.csv` to populate this table._ | | | | | | | | |

> **Note on Accuracy:** The accuracy formula above is derived from missingness and therefore reflects completeness rather than true factual accuracy.
>
> **Note on Timeliness:** Reported as `N/A` when the dataset does not contain a usable timestamp or datetime column.

---

### Governance Guidelines

**Versioning**
- Use separate commits for: raw data ingestion, cleaned data output, and dashboard changes.
- Commit messages must clearly state what was changed and why.

**Reproducibility**
- All processing steps must be documented in the Colab notebook.
- Do not rely on manual steps that are not recorded in code.

**Security**
- Do not commit Kaggle API keys, GitHub tokens, or any credentials to the repository.
- Store secrets in environment variables or a local `.env` file that is excluded via `.gitignore`.

**Data Integrity**
- Raw data in `data/raw/` must never be modified.
- All transformations must be written exclusively to the `outputs/` directory.

---

## Evidence (Screenshots)

Place evidence screenshots in the following paths before final submission:

| File | Content |
|---|---|
| `docs/screenshots/dashboard.png` | Streamlit dashboard (full view) |
| `docs/screenshots/eda.png` | EDA output from Colab |
| `docs/screenshots/analysis.png` | Cleaning or analysis step from Colab |

---

## Auto-Generate README from Colab

To automatically populate the data quality table in this README from `outputs/data_quality_metrics.csv`, run the following script inside your Colab environment:

```python
import os
import pandas as pd

REPO_DIR = "/content/data-lifecycle-smart-agriculture-23082010054"
README_PATH = os.path.join(REPO_DIR, "README.md")
METRICS_PATH = os.path.join(REPO_DIR, "outputs", "data_quality_metrics.csv")

if os.path.exists(METRICS_PATH):
    m = pd.read_csv(METRICS_PATH)

    def fmt(x):
        try:
            return "N/A" if pd.isna(x) else f"{float(x):.4f}"
        except Exception:
            return str(x)

    rows = ""
    for _, r in m.iterrows():
        rows += (
            f"| {r.get('dataset', '')} "
            f"| {int(r.get('rows', 0))} "
            f"| {int(r.get('cols', 0))} "
            f"| {int(r.get('missing_cells', 0))} "
            f"| {int(r.get('total_cells', 0))} "
            f"| {fmt(r.get('accuracy'))} "
            f"| {fmt(r.get('completeness'))} "
            f"| {fmt(r.get('timeliness_30d'))} "
            f"| {r.get('timeliness_note', '')} |\n"
        )

    print("Metrics loaded. Update the Data Quality Results table in README.md with the rows above.")
    print(rows)
else:
    print("File not found:", METRICS_PATH)
```

After updating the README, commit and push:

```bash
cd /content/data-lifecycle-smart-agriculture-23082010054
git add README.md
git commit -m "docs: update README with data quality metrics"
git push origin main
```
