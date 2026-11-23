# 💧 HydroSense AI

### AI-Based Condition Monitoring and Fault Diagnosis of Industrial Hydraulic Systems Using Machine Learning

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow)
![Dataset License](https://img.shields.io/badge/Dataset%20License-CC%20BY%204.0-green)
![Focus](https://img.shields.io/badge/Focus-Predictive%20Maintenance-orange)

---

## 📌 Overview

**HydroSense AI** is a Machine Learning project that analyzes multisensor data from an industrial hydraulic system to identify the **condition and degradation level** of its components (cooler, valve, pump, accumulator).

Instead of only answering *"Is the machine working or broken?"*, HydroSense AI predicts **how healthy each component is**, which supports earlier and better-informed maintenance decisions.

---

## ❗ Problem Statement

Hydraulic systems are used in manufacturing machinery, industrial presses, construction equipment, and production lines. Their components (pumps, valves, coolers, accumulators) degrade over time because of wear, leakage, temperature changes, and continuous operation.

Traditional maintenance (periodic inspection or fixing after failure) can cause:

- Unexpected equipment failures
- Production interruptions
- Higher maintenance costs
- Reduced operational efficiency

**Research question:**
> How can Machine Learning techniques analyze sensor measurements from an industrial hydraulic system to identify the condition and degradation level of its components?

---

## 💡 Proposed Solution

HydroSense AI analyzes measurements from multiple sensors (pressure, temperature, vibration, motor power, and fluid flow) and trains ML models to classify the condition of hydraulic components.

Example: classifying the **valve** into one of four conditions:

| Class | Meaning |
|-------|---------|
| Optimal switching | Valve works normally |
| Small switching delay | Early-stage degradation |
| Severe switching delay | Advanced degradation |
| Near-total switching failure | Close to failure |

---

## 📊 Dataset

| Item | Details |
|------|---------|
| **Name** | Condition Monitoring of Hydraulic Systems |
| **Source** | [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/447/condition+monitoring+of+hydraulic+systems) |
| **License** | CC BY 4.0 (attribution required) |
| **Operating cycles** | 2,205 |
| **Sensor channels** | 17 |
| **Measurements per cycle** | 43,680 |
| **Cycle duration** | 60 seconds |
| **Origin** | Real experimental hydraulic test rig |

### Input Features (X)

| Sensors | Measures |
|---------|----------|
| PS1–PS6 | Hydraulic pressure |
| EPS1 | Motor power consumption |
| FS1–FS2 | Fluid flow |
| TS1–TS4 | Fluid temperature |
| VS1 | Vibration |
| CE, CP, SE | Virtual sensors (cooling efficiency, cooling power, system efficiency) |

### Target Variables (Y)

| Component | Condition being predicted |
|-----------|---------------------------|
| Cooler | Cooling efficiency level |
| Valve | Switching performance level |
| Pump | No leakage / weak leakage / severe leakage |
| Accumulator | Pressure level |

The project can focus on one component or cover all four.

---

## 🔄 Machine Learning Pipeline

1. **Data Understanding:** hydraulic system, sensors, labels, how data was collected
2. **Exploratory Data Analysis (EDA):** distributions, sensor patterns, correlations, class distributions
3. **Data Cleaning:** missing values, duplicates, outliers, consistency across sensor files
4. **Data Integration & Feature Engineering:** merge sensor files; extract Mean, Std, Min, Max, RMS; remove redundant features
5. **Preprocessing:** target encoding, scaling, class imbalance handling, train/test split that respects the cycle structure
6. **Model Development:** Logistic Regression, Decision Tree, Random Forest, SVM, XGBoost
7. **Model Evaluation:** Accuracy, Precision, Recall, F1-score, Confusion Matrix
8. **Model Interpretation:** feature importance to find the most informative sensors

---

## 🔬 Planned Experiments (Potential Contributions)

- Raw sensor signals vs. statistical feature extraction
- Comparison of multiple ML algorithms
- Which sensors matter most for fault diagnosis
- Effect of class imbalance on model performance
- Ability to detect **early-stage degradation**

> The final contributions depend on the experimental results.

---

## 🗂️ Project Structure

```
HydroSense-AI/
├── data/
│   ├── raw/              # Original UCI files (not tracked by Git)
│   └── processed/        # Engineered feature tables
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_cleaning.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_modeling.ipynb
│   └── 06_interpretation.ipynb
├── src/                  # Reusable Python modules
├── models/               # Saved trained models
├── reports/
│   └── figures/          # Plots and charts
├── requirements.txt
├── .gitignore
└── README.md
```

> This is the planned layout; adjust it to match your actual repository.

---

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/omardiab9951/HydroSense-AI.git
cd HydroSense-AI

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Suggested `requirements.txt`

```
numpy
pandas
scipy
matplotlib
seaborn
scikit-learn
xgboost
imbalanced-learn
shap
jupyter
```

### Get the data

1. Download the dataset from the [UCI page](https://archive.ics.uci.edu/dataset/447/condition+monitoring+of+hydraulic+systems).
2. Extract the files into `data/raw/`.

---

## 🚀 Usage

```bash
jupyter notebook
```

Run the notebooks in `notebooks/` in numerical order (01 → 06).

---

## 📈 Results

*Results will be added after the experiments are completed.*

| Model | Accuracy | Precision | Recall | F1-score |
|-------|----------|-----------|--------|----------|
| Logistic Regression | – | – | – | – |
| Decision Tree | – | – | – | – |
| Random Forest | – | – | – | – |
| SVM | – | – | – | – |
| XGBoost | – | – | – | – |

---

## 🗺️ Roadmap

- [ ] Data understanding
- [ ] Exploratory data analysis
- [ ] Data cleaning
- [ ] Feature engineering
- [ ] Preprocessing and train/test split
- [ ] Model training and comparison
- [ ] Evaluation and error analysis
- [ ] Model interpretation
- [ ] Final report / research paper

---

## ⚠️ Scope and Limitations

- This project is **offline ML experimentation** on the public UCI dataset.
- It does **not** connect to physical machinery or run a live monitoring system.
- The data comes from an **experimental hydraulic test rig**, not from an Egyptian factory. Results demonstrate a methodology that could apply to industrial facilities in Egypt, but performance on real factory equipment would require further validation.
- The project performs **component condition classification**. It does **not** predict exact failure times or Remaining Useful Life (RUL).

---

## 📚 Citation and Attribution

This project uses the dataset released under CC BY 4.0. Please attribute the original authors:

> Helwig, N., Pignanelli, E., & Schütze, A. (2015). *Condition Monitoring of Hydraulic Systems* [Dataset]. UCI Machine Learning Repository.
> https://archive.ics.uci.edu/dataset/447/condition+monitoring+of+hydraulic+systems

---

## 👤 Author

**Omar Diab**
GitHub: [@omardiab9951](https://github.com/omardiab9951)

---

## 📄 License

Code: choose a license for your own code (e.g., MIT) and add a `LICENSE` file.
Dataset: CC BY 4.0, owned by its original authors.
