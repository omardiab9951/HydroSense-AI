# HydroSense AI — Master Progress Report

## Project at a glance

| Item | Details |
|---|---|
| Project | HydroSense AI |
| Goal | Condition monitoring and fault diagnosis of industrial hydraulic systems |
| Dataset | UCI Condition Monitoring of Hydraulic Systems; one experimental hydraulic test rig |
| Dataset license | CC BY 4.0 |
| Project dates | 22 Nov–20 Dec 2026 |
| Current status | Sprint 1 complete; Sprints 2–4 not started |

## Goal

Understand the UCI hydraulic-system sensor data and then develop a careful, reproducible condition-monitoring workflow. Sprint 1 documents the data and reports exploratory findings. Later sprint work must distinguish test-rig condition labels from chronological deterioration; this dataset does not establish a failure timeline or generalize automatically to other rigs.

## Progress snapshot

| Sprint | Dates | Original sprint name | Status | Completion |
|---|---|---|---|---:|
| Sprint 1 | 22–28 Nov | Data understanding and EDA | Complete | 100% |
| Sprint 2 | 29 Nov–5 Dec | Data cleaning and feature engineering | Not started | 0% |
| Sprint 3 | 6–12 Dec | ML model development | Not started | 0% |
| Sprint 4 | 13–20 Dec | Evaluation, interpretation, finalization | Not started | 0% |

## Decisions and working principles

- `dataset/raw` is read-only. Findings are reported; data are not removed, clipped, or modified during Sprint 1.
- Sprint 1 is descriptive only: no feature-engineering dataset, train/test split, scaling, or model training.
- The per-cycle summary cache is for EDA only and is not the Sprint 2 feature dataset.
- Condition levels are set on a test rig. They must not be described as early-stage degradation detection or chronological failure progression.
- Row order is grouped by condition; future splitting must account for this rather than rely on row slicing.
- The dataset represents a single experimental test rig; transfer to other equipment is not established.
- Review fields are for the student to complete at sprint review.

## Sprint 1 — Data understanding and EDA (22–28 Nov)

**Status:** Complete — 100%

### Checklist

- [x] Audit the raw-data folder and record its integrity baseline.
- [x] Describe sensors and targets from project configuration.
- [x] Validate file shapes and missing values.
- [x] Inspect the profile, sensor slices, and cycle alignment by row position.
- [x] Report class counts, percentages, and imbalance.
- [x] Count label combinations and compare row ordering with random-order expectations.
- [x] Report data-quality checks without modifying data.
- [x] Build the per-cycle EDA-only cache for all 17 sensors.
- [x] Produce descriptive statistics and sensor-mean distribution plots.
- [x] Produce controlled raw-signal examples and class-average overlays.
- [x] Analyze sensor correlations and sensor-to-target relationships.
- [x] Compare selected sensor means by stable flag.
- [x] Report IQR outlier counts without removing values.
- [x] Execute both notebooks with saved outputs.
- [x] Write the Sprint 1 dataset-understanding report.

### Deliverables

- [x] `notebooks/01_Data_Understanding.ipynb`
- [x] `notebooks/02_EDA.ipynb`
- [x] `reports/results/`
- [x] `reports/figures/`
- [x] `dataset/processed/eda_cycle_summary.parquet` (EDA-only cache)
- [x] `docs/Sprint1_Dataset_Understanding_Report.md`

### Experiment log

| Date | Work | Result |
|---|---|---|
| 2026-11-22 | Audit raw files | 20 files, 530.5 MiB; raw data left unchanged. |
| 2026-11-22 | Run helper smoke test and cycle-summary computation | Low-rate smoke test passed; all 17 sensors summarized into 2205 rows and 68 mean/std/min/max columns. |
| 2026-11-22 | Execute data-understanding notebook | Completed with saved outputs using the `hydrosense` kernel. |
| 2026-11-22 | Execute EDA notebook | Completed with saved outputs, result tables, and figures using the `hydrosense` kernel. |
| 2026-11-22 | Correct notebook imports and rerun both notebooks | Added the required `src` imports after setup; both notebooks completed top to bottom without saved error outputs. |
| 2026-11-22 | Write Sprint 1 report and update project documentation | Report, results, figures, README instructions, and this progress record updated. |

### Findings and notes

- The raw folder contains 20 files totaling 530.5 MiB. All 17 sensor files and `profile.txt` have 2205 rows aligned by row position.
- No NaN or infinite values or row-count mismatches were found.
- Class counts were cooler 732/732/741 (largest/smallest ratio 1.012); valve 360/360/360/1125 (3.125); pump 1221/492/492 (2.482); accumulator 808/399/399/599 (2.025); stable 1449/756 (1.917).
- The four component targets have 144 unique label combinations. Adjacent-row changes were cooler 2, valve 144, pump 36, and accumulator 11; all are far below the random-shuffle expectations.
- PS4 has 1237 duplicate complete cycles and 1238 constant cycles. PS3 has 26 constant columns; SE has 8.
- PS5 and PS6 per-cycle means have Pearson r = 0.999993. Temperature means TS1–TS4 are also highly correlated with one another (Pearson r from 0.9983 to 0.9997).
- CE and CP have Spearman correlations of 0.942 and 0.942 with cooler labels. TS1–TS4 have correlations from -0.929 to -0.936 with cooler labels. Selected accumulator relationships are weaker: PS2 -0.302 and PS1 -0.283.
- Stable-flag counts are 1449 for stable=0 and 756 for stable=1. Mean values for stable=0 versus stable=1 were: CE 31.427 vs 31.054, PS2 110.124 vs 107.953, EPS1 2509.781 vs 2468.156, and TS1 45.592 vs 45.104. These are descriptive differences only.
- Findings apply to a single experimental test rig; condition labels do not imply chronological failure progression.

### Sprint review

- Sprint review: _Add at sprint review._
- What went well: _Add at sprint review._
- What was difficult: _Add at sprint review._
- Student reflection: _Add at sprint review._

## Sprint 2 — Data cleaning and feature engineering (29 Nov–5 Dec)

**Status:** Not started — 0%

### Checklist

- [ ] Complete the planned data-cleaning and feature-engineering work.
- [ ] Document decisions and validate any Sprint 2 dataset separately from the EDA-only cache.

### Deliverables

- [ ] Sprint 2 deliverables — _Not completed or recorded._

### Experiment log

No Sprint 2 experiments recorded; the sprint has not started.

### Open questions carried from Sprint 1

- Determine whether and how to handle the 1237 duplicate complete cycles and 1238 constant cycles on PS4. Sprint 1 did not remove or alter them.
- Review the observed sensor ranges and constant columns before making any cleaning decision.
- Define a split strategy that accounts for grouped condition order and preserves condition coverage.

### Sprint review

- Sprint review: _Add at sprint review._
- What went well: _Add at sprint review._
- What was difficult: _Add at sprint review._
- Student reflection: _Add at sprint review._

## Sprint 3 — ML model development (6–12 Dec)

**Status:** Not started — 0%

### Checklist

- [ ] Complete the planned ML model development work.
- [ ] Record model experiments and results when they are run.

### Deliverables

- [ ] Sprint 3 deliverables — _Not completed or recorded._

### Experiment log

No Sprint 3 experiments recorded; the sprint has not started.

### Sprint review

- Sprint review: _Add at sprint review._
- What went well: _Add at sprint review._
- What was difficult: _Add at sprint review._
- Student reflection: _Add at sprint review._

## Sprint 4 — Evaluation, interpretation, finalization (13–20 Dec)

**Status:** Not started — 0%

### Checklist

- [ ] Complete the planned evaluation, interpretation, and finalization work.
- [ ] Record final results and limitations after evaluation is performed.

### Deliverables

- [ ] Sprint 4 deliverables — _Not completed or recorded._

### Experiment log

No Sprint 4 experiments recorded; the sprint has not started.

### Sprint review

- Sprint review: _Add at sprint review._
- What went well: _Add at sprint review._
- What was difficult: _Add at sprint review._
- Student reflection: _Add at sprint review._

## Final results

| Sprint | Result to date | Status |
|---|---|---|
| Sprint 1 — Data understanding and EDA | Dataset inventory, validated data profile, quality and label-order findings, EDA-only cycle summary, result tables, figures, executed notebooks, and report completed. | Complete |
| Sprint 2 — Data cleaning and feature engineering | No results recorded. | Not started |
| Sprint 3 — ML model development | No results recorded. | Not started |
| Sprint 4 — Evaluation, interpretation, finalization | No results recorded. | Not started |
