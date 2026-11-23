# Sprint 1 - Dataset Understanding Report

## 1. Dataset overview

The project uses the UCI Condition Monitoring of Hydraulic Systems dataset, licensed under CC BY 4.0. The data come from an industrial hydraulic test rig and contain 2205 operating cycles. Each row represents one 60-second cycle, for a total of 17 sensor files aligned with 2205 condition-profile rows. Sensor attribution should include Nikolai Helwig, Eliseo Pignanelli, Andreas Schutze, and ZeMA gGmbH.

## 2. Files and row alignment

The raw folder has 20 files and is 530.5 MiB: 17 sensor files, `profile.txt`, `description.txt`, and `documentation.txt`. All 17 sensor arrays have 2205 rows, and each file matches the same cycle position in `profile.txt`; there is no ID column. The raw data are unchanged and remain read-only.

The sensors cover pressure (PS1-PS6), motor power (EPS1), flow (FS1-FS2), temperature (TS1-TS4), vibration (VS1), virtual cooling (CE and CP), and efficiency (SE). High-rate pressure and power files contain 6000 samples per cycle; flow files contain 600; the remaining 1 Hz files contain 60.

## 3. Targets and class balance

| Target | Meaning of values | Classes | Counts |
|---|---|---:|---|
| cooler | 3 near failure; 20 reduced efficiency; 100 full efficiency | 3 | 732, 732, 741 |
| valve | 73 near failure; 80 severe lag; 90 small lag; 100 optimal | 4 | 360, 360, 360, 1125 |
| pump | 0 none; 1 weak; 2 severe leakage | 3 | 1221, 492, 492 |
| accumulator | 90 near failure; 100 severely reduced; 115 slightly reduced; 130 optimal | 4 | 808, 399, 399, 599 |
| stable | 0 stable; 1 static conditions may not have been reached | 2 | 1449, 756 |

The largest/smallest class ratios are 1.012 for cooler, 3.125 for valve, 2.482 for pump, 2.025 for accumulator, and 1.917 for stable. Valve has the largest imbalance.

## 4. Label combinations and row order

The four component conditions occur in 144 unique combinations. Counts range from 10 to 230 cycles. Adjacent-row value changes are 2 for cooler, 144 for valve, 36 for pump, and 11 for accumulator. In contrast, the random-shuffle expectations are about 1469, 1454, 1309, and 1601 changes, respectively. The labels are clearly grouped by row rather than randomly shuffled.

This matters for splitting in later work: use a split method that preserves condition coverage and does not rely on the order of rows or on a simple row slice.

## 5. Data quality

No NaN or infinite values were found. No sensor had missing or mis-sized data. Duplicated complete cycles total 1237, all on PS4. PS4 also has 1238 constant cycles. Constant columns total 34 (26 in PS3 and 8 in SE). The PS2 observed range includes 0 bar, FS1 includes 0 l/min, and SE reaches 100.6%. These findings are recorded for later handling decisions; no clipping, removal, or data modification is performed in Sprint 1.

IQR report results include 240 outliers in the per-cycle means of PS1, PS2, PS3, FS1, and SE; 532 for PS4 mean; 10 for EPS1 mean; and 5 for VS1 mean. PS2 cycle maximum has 46 IQR outliers. The IQR rule is descriptive and may identify real operating behavior.

## 6. Key EDA findings

- See `02_sensor_mean_distributions_*.png` for per-cycle mean distributions.
- See `03_cooler_*`, `04_valve_*`, `05_pump_*`, and `06_accumulator_*` for controlled raw signal examples. Exact example row indices are saved in `reports/results/example_cycle_rows.csv`.
- See `07_mean_overlay_*.png` for class-average signals.
- The strongest Pearson correlation is PS5 versus PS6 at 0.999993, and the TS1-TS4 temperature means are also highly correlated. The heatmap is `08_sensor_mean_correlation_heatmap.png`.
- Cooler has strong Spearman relationships with CE and CP (about 0.942), while selected accumulator relationships are weaker.
- Stable=0 and stable=1 have different means for PS2 (110.124 versus 107.954) and EPS1 (2509.781 versus 2468.156), but this observation is not a causal conclusion.

Condition levels are settings or states from a test rig. They do not describe a chronological failure progression. This work applies to a single experimental test rig, not automatically to all factory equipment.

## 7. Open questions and risks

- How should grouped rows and condition coverage be handled in the later split strategy?
- How should PS4 duplicate and constant cycles be handled by Sprint 2 without bias or loss of intended conditions?
- Are 0 and 100.6% measurements physically plausible for the relevant sensors, or do they indicate sensor-state artifacts?
- Should highly correlated sensors be reduced or regularized later, while preserving interpretability?
- Stable flag interpretation requires care because it describes whether static conditions may not have been reached.
