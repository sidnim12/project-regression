# Energy Production Forecasting (Time Series Regression)

Forecast hourly energy production using a leakage-safe, phase-driven time-series regression pipeline.  
This repo prioritizes **methodology, reproducibility, and robustness** over brute-force tuning.

---

## Why this matters

Accurate energy production forecasting supports:
- grid stability and load balancing  
- capacity planning  
- reliable integration of renewables (high variability)

This project is structured the way real forecasting work is done:
**chronological splits, leakage prevention, baselines, robust evaluation, and diagnostics**.

---

## Dataset

- **Type:** Hourly time-series (tabular)
- **Target:** `Production`
- **Features:** time-derived signals + categorical context (e.g., source/season/day name)
- **Source:** Kaggle (download separately)

> Place the dataset file(s) inside `data/` (ignored by git).

---

## Project Phases (Notebook-driven)

Each phase is documented with intent → code → results → interpretation.

1. **Phase 0:** Problem framing + metric selection (RMSE)
2. **Phase 1:** Data understanding + sanity checks
3. **Phase 2:** Chronological split (70/15/15) + leakage discipline
4. **Phase 3:** Baselines (Mean, Ridge)
5. **Phase 4:** Preprocessing pipelines (scaling + one-hot encoding inside Pipeline)
6. **Phase 5:** Feature engineering (lag + rolling statistics, leakage-safe shifting)
7. **Phase 6:** Advanced models (non-linear regressors)
8. **Phase 7:** Error analysis (residual system + failure modes)
9. **Phase 8:** Stability & robustness checks
10. **Phase 9:** Final model consolidation (Train + Val → Test)
11. **Phase 10:** Walk-forward validation (rolling-origin evaluation)

---

## Models Evaluated

- Mean baseline
- Ridge Regression (pipeline-based)
- Random Forest Regressor
- **HistGradientBoosting Regressor (final choice)**

---

## Feature Engineering Highlights (Leakage-safe)

Forecasting features were engineered using *only past information*:

- **Lag features:** `lag_1`, `lag_24`
- **Rolling stats:** `24h rolling mean` computed from shifted values  
- Strict rule: features at time **t** use only information from **t-1 and earlier**

---

## Evaluation Strategy

- **Primary metric:** RMSE
- **Validation:** used for model selection and comparison
- **Test:** used only for final unbiased evaluation
- **No shuffling** (time integrity preserved)
- **Walk-forward validation** added to verify robustness across multiple time windows

---

## Key Results (RMSE)

### Fixed-split progression (chronological split)
- **Mean baseline:** ~4474  
- **Ridge:** ~4434  
- **HistGradientBoosting (train-only) Test RMSE:** ~2381  
- **Final consolidated model (Train + Val → Test): ~2339.96**

### Walk-forward validation (Phase 10)
- Mean RMSE across folds: **<paste results_df mean here>**
- Std RMSE across folds: **<paste results_df std here>**
- Best / Worst fold RMSE: **<paste min / max here>**

**Interpretation:** stable mean with low variance indicates the model is not dependent on a single favourable split and generalizes across time windows.

---

## Error Analysis & Robustness

Beyond aggregate RMSE, this project includes:
- residual distribution checks (bias / skew)
- RMSE by hour of day (peak-hour stress)
- RMSE by predicted bins (heteroscedasticity)
- temporal drift checks (stability across evaluation windows)

This validates that improvements are real and operationally meaningful.

---

## Deployment Notes (How this can go live)

This project is structured to be production-friendly:
- preprocessing + model encapsulated in a **single sklearn Pipeline**
- deterministic feature engineering
- realistic evaluation mirrors deployment constraints

With minimal extension:
- serialize model via `joblib`
- serve via FastAPI/Flask for real-time inference
- schedule batch predictions + periodic retraining for new data

---

## Repository Structure

```text
project-regression/
├── data/                 # dataset files (ignored in git)
├── notebooks/            # phase-by-phase notebooks
├── README.md
├── requirements.txt
└── .gitignore
```
---
## How to Run
1️⃣ Clone the repository:
```bash
git clone https://github.com/sidnim12/project-regression.git
cd project-regression
```


2️⃣ Create a virtual environment (recommended):

```bash
python -m venv venv
```

Activate it:

Windows:
```bash
venv\Scripts\activate
```
Mac/Linux: 
```bash
source venv/bin/activate
```

3️⃣ Install dependencies:
```bash
pip install -r requirements.txt
```

Add the dataset:
Download the dataset from Kaggle and place the CSV file inside the data/ folder 
example structure
```text
project-regression/
├── data/
│   └── energy_production.csv
```

4️⃣ Run the notebooks:
```bash
jupyter notebook
```

Open notebooks in order from Phase 0 through Phase 10.

Expected outputs:
- Validation RMSE comparison
- Final Test RMSE 
- Walk-forward mean/std RMSE,
- residual/stability plots.

---

## 👤 Author

**Sai Sidhardh Nimishakavi**

Machine Learning Practitioner focused on structured, leakage-safe time-series modeling and real-world forecasting systems.

This project reflects disciplined ML methodology, robust evaluation practices, and deployment-aware design.

📫 GitHub: [sidnim12](https://github.com/sidnim12)  
🔗 LinkedIn: [Sai Sidhardh Nimishakavi](https://www.linkedin.com/in/sai-sidhardh-nimishakavi-8132b6372)
