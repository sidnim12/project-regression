# Energy Production Forecasting — Time Series Regression

## Overview
This project focuses on forecasting **hourly energy production** using historical data and time-based contextual features.  
The objective is to build a **leakage-safe, interpretable, and well-structured time-series regression pipeline**, while analyzing where and why models fail.

The project emphasizes **methodology and reasoning** over brute-force modeling, following practices used in real-world ML systems.

---

## Problem Statement
Accurate energy production forecasting is critical for:
- grid stability and load balancing
- capacity planning
- efficient integration of renewable energy sources

Given historical production data with temporal and categorical context, the task is to predict future energy production values while respecting time dependencies and avoiding data leakage.

---

## Dataset
- Hourly time-series dataset
- Target variable: `Production`
- Feature types:
  - Temporal: hour, day of year
  - Categorical: season, energy source, day name
- Data is **time-ordered** and treated as a forecasting problem

> Dataset source: Kaggle (download separately and place in the `data/` directory)

---

## Methodology & Project Phases
The project follows a structured multi-phase workflow:

1. **Phase 0 — Problem framing & metric selection**
2. **Phase 1 — Data understanding & sanity checks**
3. **Phase 2 — Time-aware train/validation/test split**
4. **Phase 3 — Baseline models (mean, Ridge regression)**
5. **Phase 4 — Preprocessing pipelines (numerical + categorical)**
6. **Phase 5 — Feature engineering (lag & rolling statistics)**
7. **Phase 6 — Advanced non-linear models**
8. **Phase 7 — Error analysis & failure modes** *(in progress)*
9. **Phase 8 — Stability & robustness checks**
10. **Phase 9 — Conclusions & future work**

Each phase is documented directly in the notebook with clear intent, results, and interpretation.

---

## Models Evaluated
- Mean baseline
- Ridge Regression
- Random Forest Regressor
- HistGradientBoosting Regressor (best performer)

---

## Feature Engineering Highlights
- Lag features:
  - 1-hour lag
  - 24-hour lag
- Rolling statistics:
  - 24-hour rolling mean
- Strict leakage prevention using shifted values only

---

## Evaluation Metric
- **RMSE (Root Mean Squared Error)**
- Validation set is used for model selection
- Test set reserved for final evaluation only

---

## Key Results (Validation RMSE)
| Model | RMSE |
|-----|------|
| Ridge (with lag features) | ~4350 |
| Random Forest | ~4566 |
| HistGradientBoosting | ~4031 |

HistGradientBoosting achieved the best performance, indicating the importance of combining **temporal feature engineering** with **non-linear modeling**.

---

## Error Analysis (Ongoing)
Current analysis focuses on:
- temporal drift in residuals
- peak-hour error behavior
- season-wise and source-wise failure patterns

This phase aims to move beyond aggregate metrics and understand **model limitations**.

---

## Repository Structure
project-regression/
├── data/                     # Dataset files (ignored in git)
├── notebooks/
│   └── energy_production.ipynb   # Main analysis notebook
├── README.md                 # Project overview and documentation
├── requirements.txt          # Python dependencies
└── .gitignore                # Ignored files and folders


---

## How to Run
1. Clone the repository
2. Download the dataset and place it in `data/`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Open the notebook
   ```bash
   jupyter notebook notebooks/energy-production.ipynb

## Notes
- The project prioritizes correct time-series handling and interpretability
- No random shuffling is used at any stage
- Feature engineering and model complexity are introduced incrementally
---
## Future Work
- Incorporate external signals (e.g., weather data)
- Perform rolling-origin cross-validation
- Extend analysis to probabilistic forecasting
- Package insights into a lightweight analysis tool

---

## Author
Developed as part of a self-directed ML study project with the goal of building research-oriented machine learning work.

