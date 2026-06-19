# 💼 Pay Equity Lens

> **Corporate HR Pay Equity & Salary Benchmarking using Machine Learning**

A complete end-to-end Data Analytics project that detects gender pay gaps and benchmarks fair salaries across a 1,470-employee corporate HR dataset — combining exploratory analysis, ML-driven salary prediction, and an interactive Power BI dashboard.

---

## 🎯 Problem Statement

Organizations often suffer from **structural pay inequities** that go undetected without data-driven analysis. This project answers:

1. Is there a measurable gender pay gap at this organization?
2. Which departments and roles show the most severe underpayment?
3. Can we predict what an employee *should* earn based on their qualifications — and flag those being paid unfairly?

---

## 📊 Key Findings

| Metric | Value |
|---|---|
| Overall Gender Pay Gap | **9.2%** |
| Male Average Monthly Salary | $15,810 |
| Female Average Monthly Salary | $14,351 |
| % Female Employees Underpaid | **16.9%** |
| % Male Employees Underpaid | 9.8% |
| Most Underpaid Department | Human Resources (21.6%) |
| Strongest Salary Predictor | Job Level (r = 0.85) |

> **Bottom line:** A statistically significant pay gap exists and persists even after controlling for job level, experience, and education — suggesting structural bias rather than merit-based differences.

---

## 🗂️ Project Structure

```
pay-equity-lens/
├── data/
│   ├── raw/                    # Original HR dataset (1,470 employees)
│   ├── processed/              # Cleaned data + model predictions
│   └── README.md               # Dataset documentation & column guide
├── notebooks/
│   ├── 01_EDA.ipynb            # Exploratory Data Analysis
│   ├── 02_insights.ipynb       # Deep dive + ML model training
│   └── 03_recommendations.ipynb # Business recommendations
├── src/
│   ├── data_loader.py          # Reusable data loading utilities
│   └── visualizations.py       # Reusable plotting functions (dark theme)
├── model/
│   ├── salary_predictor.py     # Full ML pipeline (train → predict → flag)
│   ├── salary_rf_model.pkl     # Saved Random Forest model
│   └── model_results.json      # Evaluation metrics for all models
├── dashboard/
│   └── powerbi_guide.md        # Step-by-step Power BI build guide
├── reports/                    # All generated charts (PNG)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🔬 Methodology

### 1. Data Preparation
- 1,470 employee records, 19 features
- No null values or duplicates
- Ordinal encoding for Education, Job Level, Satisfaction scores

### 2. Exploratory Data Analysis
- Salary distribution analysis (histogram, mean/median)
- Gender pay gap by department, job level, and role
- Correlation matrix to identify salary drivers
- Scatter analysis of salary vs. experience

### 3. Salary Benchmarking Model
Four regression models trained to predict "fair market salary":

| Model | MAE | RMSE | R² |
|---|---|---|---|
| Linear Regression | $915 | $1,121 | 0.8935 |
| Ridge Regression | $918 | $1,124 | 0.8928 |
| **Random Forest** | **$661** | **$884** | **0.9338** |
| Gradient Boosting | $608 | $810 | 0.9444 |

**Random Forest selected** for its balance of accuracy, interpretability, and feature importance output.

### 4. Pay Equity Flagging
Employees whose actual salary deviates from the model prediction by **more than $500** are flagged:
- **Underpaid:** Actual < Predicted − $500
- **Overpaid:** Actual > Predicted + $500

---

## 📈 Charts & Visualizations

| Chart | Description |
|---|---|
| `fig1_pay_distribution.png` | Income histogram + gender comparison |
| `fig2_pay_gap_breakdown.png` | Gap by department and job level |
| `fig3_salary_experience.png` | Salary vs. experience scatter + role gap |
| `fig4_correlation.png` | Feature correlation heatmap |
| `fig5_model_results.png` | Feature importance + actual vs. predicted |
| `fig6_pay_equity.png` | Underpaid % by gender and department |

---

## 🖥️ Power BI Dashboard

Built in **Power BI Desktop** with 3 pages:

- **Page 1:** Executive Overview — KPI cards, department breakdown, pay status donut
- **Page 2:** Pay Gap Deep Dive — job level trends, scatter plots, role-wise gap
- **Page 3:** Underpaid Employee Analysis — actionable employee-level table



---

## 💡 Business Recommendations

1. **Immediate Pay Audit** — 16.9% of female employees are underpaid >$500 vs their predicted fair salary. Prioritize corrections.
2. **Standardize Salary Bands** — Use model predictions as midpoint benchmarks for transparent pay ranges per role + level.
3. **Fix HR Department Pay** — HR has the highest underpayment rate (21.6%) and lowest avg salary. Urgent market alignment needed.
4. **Sales Base-Pay Review** — 16.5% underpayment may be hidden by commission structures.
5. **Quarterly Model Runs** — Deploy salary predictor quarterly; auto-flag employees falling 10%+ below benchmark.

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.10+ |
| Data | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| ML | Scikit-learn (LinearRegression, Ridge, RandomForest, GradientBoosting) |
| Notebooks | Jupyter |
| Dashboard | Power BI Desktop + Power BI Service |

---

## 🚀 Getting Started

```bash
git clone https://github.com/apoorva-s9091/pay-equity-lens.git
cd pay-equity-lens

pip install -r requirements.txt

# Run EDA
jupyter notebook notebooks/01_EDA.ipynb

# Train model & generate predictions
python model/salary_predictor.py
```

---

## 📁 Dataset

Synthetic HR dataset (1,470 employees) modeled after the IBM HR Analytics dataset.  
See [`data/README.md`](data/README.md) for full column documentation and limitations.

---

## 👩‍💻 Author

**Apoorva**  
B.Tech CSE (Data Science) | PSIT Kanpur  
[GitHub](https://github.com/apoorva-s9091) · [LinkedIn](#)

---

*This project is for educational and portfolio purposes.*
