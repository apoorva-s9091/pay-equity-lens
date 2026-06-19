# Power BI Dashboard Guide — Pay Equity Lens

## Overview
This guide walks you through building the **Pay Equity Lens** dashboard in Power BI Desktop using the processed dataset. Follow this step-by-step to recreate the full interactive dashboard.

---

## Step 1: Load the Data

1. Open **Power BI Desktop**
2. Click **Get Data → Text/CSV**
3. Select `data/processed/hr_with_predictions.csv`
4. Click **Load**

---

## Step 2: Data Transformations (Power Query)

Go to **Transform Data** and apply:

| Column | Transformation |
|---|---|
| `MonthlyIncome` | Change type → Whole Number |
| `PredictedFairSalary` | Change type → Whole Number |
| `SalaryGap` | Change type → Whole Number |
| `Underpaid` | Change type → True/False |
| `Overpaid` | Change type → True/False |

Click **Close & Apply**.

---

## Step 3: Create Measures (DAX)

Go to **Home → New Measure** and create these:

```dax
Total Employees = COUNTROWS('hr_with_predictions')

Avg Salary = AVERAGE('hr_with_predictions'[MonthlyIncome])

Male Avg Salary = 
CALCULATE(AVERAGE('hr_with_predictions'[MonthlyIncome]),
          'hr_with_predictions'[Gender] = "Male")

Female Avg Salary = 
CALCULATE(AVERAGE('hr_with_predictions'[MonthlyIncome]),
          'hr_with_predictions'[Gender] = "Female")

Gender Pay Gap % = 
DIVIDE([Male Avg Salary] - [Female Avg Salary], [Male Avg Salary]) * 100

Underpaid Count = 
CALCULATE(COUNTROWS('hr_with_predictions'),
          'hr_with_predictions'[Underpaid] = TRUE())

Underpaid % = 
DIVIDE([Underpaid Count], [Total Employees]) * 100
```

---

## Step 4: Dashboard Layout (3 Pages)

### Page 1: Executive Overview

**Background color:** `#0f1117` (set via Format → Canvas background)

**Visuals to add:**

| Visual | Fields | Position |
|---|---|---|
| Card | Total Employees | Top-left |
| Card | Avg Salary | Top-center-left |
| Card | Gender Pay Gap % | Top-center-right |
| Card | Underpaid % | Top-right |
| Clustered Bar Chart | X: Department, Y: Avg Salary, Legend: Gender | Center-left |
| Donut Chart | Legend: PayStatus, Values: Count | Center-right |
| Slicer | Department | Left panel |
| Slicer | Gender | Left panel |

**Card formatting:**
- Font color: White
- Background: `#1a1d2e`
- Border: None

---

### Page 2: Pay Gap Deep Dive

**Visuals:**

| Visual | Fields | Note |
|---|---|---|
| Clustered Bar | X: JobLevelLabel, Y: Avg MonthlyIncome, Legend: Gender | Shows gap widens at senior levels |
| Scatter Plot | X: TotalWorkingYears, Y: MonthlyIncome, Legend: Gender | Add trend line |
| Bar Chart | X: JobRole, Y: Gender Pay Gap % (calc column) | Sort descending |
| Matrix | Rows: Department, Columns: Gender, Values: Avg MonthlyIncome | Conditional formatting on values |

**Add a calculated column for role-level gap:**
```dax
-- In Power Query: Add a custom column
-- Or create a measure filtered by job role
```

---

### Page 3: Underpaid Employee Analysis

**Visuals:**

| Visual | Fields | Note |
|---|---|---|
| Bar Chart | X: Gender, Y: Underpaid % | Highlight female bar in orange |
| Bar Chart | X: Department, Y: Underpaid % | Color by department |
| Table | Gender, Department, JobRole, MonthlyIncome, PredictedFairSalary, SalaryGap | Filter: Underpaid = TRUE |
| Bar Chart | X: JobLevelLabel, Y: Underpaid Count | Add data labels |

**Table conditional formatting:**
- `SalaryGap` column → Color scale → Red for negative values

---

## Step 5: Theming

1. Go to **View → Themes → Customize current theme**
2. Set colors:
   - Primary: `#7B5EA7`
   - Secondary: `#54A0E0`
   - Accent 1: `#E07B54`
   - Accent 2: `#5EC87B`
   - Background: `#0f1117`
   - Second background: `#1a1d2e`
3. Font: **Segoe UI** (Power BI default, works well)

---

## Step 6: Publish to Power BI Service

1. Click **Publish** (top ribbon)
2. Sign in with your Microsoft account (free)
3. Choose **My Workspace**
4. Once published, go to **app.powerbi.com**
5. Open your report → Click **File → Embed report → Website or portal**
6. Copy the **share link** → paste into your `README.md`

---

## Step 7: Export for README

1. On each page, **File → Export → Export to PDF**
2. Take screenshots of each page (Win + Shift + S)
3. Add to `reports/` folder and embed in README under **Dashboard Preview** section

---

## Tips for Polished Look

- Use **navigation buttons** to switch between pages (Insert → Buttons → Navigator)
- Add your name and date as a **text box** in the footer
- Use **tooltips** on charts to show additional context on hover
- Enable **Cross-filtering** so slicers affect all visuals on the page

---

*Pay Equity Lens | Built with Power BI Desktop | Dataset: Synthetic HR Data (1,470 employees)*
