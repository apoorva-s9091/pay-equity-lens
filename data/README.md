# Dataset Documentation

## Source
**Synthetic HR Dataset** — modeled after the IBM HR Analytics Employee Attrition & Performance dataset, widely used in the data science community for HR analytics demonstrations.

Original IBM dataset: [Kaggle — IBM HR Analytics](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)

## This Dataset
The dataset used in this project is a synthetic variant (1,470 employees) generated to preserve realistic distributions and introduce a measurable, controllable gender pay gap for analytical purposes.

## Columns

| Column | Type | Description |
|---|---|---|
| Age | int | Employee age (18–59) |
| Attrition | str | Did employee leave? (Yes/No) |
| BusinessTravel | str | Travel frequency |
| Department | str | Sales / R&D / Human Resources |
| Education | int | 1=Below College … 5=Doctor |
| EducationField | str | Field of study |
| Gender | str | Male / Female |
| JobLevel | int | 1=Junior … 5=Executive |
| JobRole | str | Specific role title |
| JobSatisfaction | int | 1=Low … 4=Very High |
| MaritalStatus | str | Single / Married / Divorced |
| MonthlyIncome | int | Monthly salary in USD |
| OverTime | str | Yes/No |
| PerformanceRating | int | 3=Excellent, 4=Outstanding |
| TotalWorkingYears | int | Career experience in years |
| TrainingTimesLastYear | int | No. of trainings attended |
| WorkLifeBalance | int | 1=Bad … 4=Best |
| YearsAtCompany | int | Tenure at company |
| YearsInCurrentRole | int | Time in current role |

## Processed Additions (hr_clean.csv)

| Column | Description |
|---|---|
| EducationLabel | Text label for Education |
| JobSatisfactionLabel | Text label for JobSatisfaction |
| WorkLifeBalanceLabel | Text label for WorkLifeBalance |
| PerformanceLabel | Text label for PerformanceRating |
| JobLevelLabel | Text label for JobLevel |

## Model Additions (hr_with_predictions.csv)

| Column | Description |
|---|---|
| PredictedFairSalary | Random Forest predicted market salary |
| SalaryGap | Actual − Predicted (negative = underpaid) |
| Underpaid | TRUE if SalaryGap < −$500 |
| Overpaid | TRUE if SalaryGap > +$500 |
| PayStatus | "Underpaid" / "Overpaid" / "Fair" |

## Limitations

1. **Synthetic data** — findings are directionally realistic but not from a real organization.
2. **Binary gender** — dataset uses Male/Female only; real HR analysis should use more inclusive categories.
3. **USD salaries** — not inflation-adjusted or region-specific.
4. **Controlled pay gap** — a 9.2% gender pay gap was intentionally embedded; real-world gaps vary by industry and region.

## License
For educational and portfolio use only.
