# HydroSense AI

## AI-Based Condition Monitoring and Fault Diagnosis of Industrial Hydraulic Systems

HydroSense AI is a Sprint 1 data-understanding and exploratory-analysis project for diagnosing component conditions in a hydraulic test rig from multivariate sensor time series. The work is based on the **UCI Condition Monitoring of Hydraulic Systems** dataset, released under **CC BY 4.0**; please attribute Nikolai Helwig, Eliseo Pignanelli, Andreas Schütze, and ZeMA gGmbH when using it.

## Project layout

```text
System/
├── dataset/
│   ├── raw/          # Downloaded source data; never modify or commit
│   └── processed/    # Cached/derived data only
├── notebooks/        # Sprint 1 understanding and EDA notebooks
├── src/              # Paths, loading, validation, and small utilities
├── models/           # Future saved model artifacts
├── reports/
│   ├── figures/      # Exported charts
│   └── results/      # Analysis outputs
└── docs/             # Project documentation
```

## Windows setup

The project notebooks use the Anaconda interpreter and the Jupyter kernel named `hydrosense`. The kernel is registered to `C:\Users\o3995\anaconda3\python.exe`.

```powershell
C:\Users\o3995\anaconda3\python.exe -m pip install -r requirements.txt
C:\Users\o3995\anaconda3\python.exe -m ipykernel install --user --name hydrosense --display-name "Python (hydrosense)"
C:\Users\o3995\anaconda3\python.exe -m jupyter lab
```

In VS Code, select **Python (hydrosense)** as the notebook kernel. The project `.venv` was removed because it did not have the required packages.

`dataset/raw` is intentionally excluded from Git. Download the UCI dataset and place its `.txt` files directly in `dataset/raw` (or keep its single extracted child directory there; `src.config` detects the folder containing `profile.txt`).

## Four-sprint plan (22 Nov – 20 Dec 2026)

1. **Sprint 1 — Data understanding and EDA** (22–28 Nov)
2. **Sprint 2 — Feature engineering and baselines** (29 Nov–5 Dec)
3. **Sprint 3 — Model development and evaluation** (6–12 Dec)
4. **Sprint 4 — Interpretation, reporting, and delivery** (13–20 Dec)

## Scope

This project supports offline experiments on a hydraulic **test-rig** dataset. It is not validated for factory equipment, does not make deployment or safety claims, classifies component conditions, and does **not** predict remaining useful life (RUL).

## Sprint 1 run instructions

Run the notebooks in order:

1. `notebooks/01_Data_Understanding.ipynb`
2. `notebooks/02_EDA.ipynb`

Use Jupyter with the `hydrosense` kernel. It is registered against `C:\Users\o3995\anaconda3\python.exe`. From the project root, either open both notebooks in JupyterLab or execute them with:

```powershell
C:\Users\o3995\anaconda3\python.exe -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3600 --ExecutePreprocessor.kernel_name=hydrosense notebooks\01_Data_Understanding.ipynb
C:\Users\o3995\anaconda3\python.exe -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=3600 --ExecutePreprocessor.kernel_name=hydrosense notebooks\02_EDA.ipynb
```

The cache `dataset/processed/eda_cycle_summary.parquet` (or CSV fallback) contains per-cycle mean, standard deviation, minimum, and maximum columns for EDA only. It is **not** a Sprint 2 feature dataset.

Sprint 1 deliverables are in:

- `notebooks/01_Data_Understanding.ipynb`
- `notebooks/02_EDA.ipynb`
- `reports/results/`
- `reports/figures/`
- `docs/Sprint1_Dataset_Understanding_Report.md`
