# Customer Churn Analysis

This project analyzes customer churn patterns using the Telco Customer Churn dataset.

The goal is to identify churn drivers, build a baseline churn model, and convert results into practical retention recommendations.

## Business Problem

A subscription-based business needs to reduce customer churn and prioritize retention actions.

The key questions:

1. What share of customers churn?
2. Which customer characteristics are linked to higher churn?
3. Which contract and payment patterns increase churn risk?
4. Can a baseline model help prioritize customers by churn risk?
5. Which customer groups should retention teams prioritize?

## Dataset

Dataset: Telco Customer Churn.

Main fields used:

| Field | Description |
|---|---|
| customerID | Unique customer identifier |
| tenure | Number of months with the company |
| Contract | Contract type |
| MonthlyCharges | Monthly payment amount |
| TotalCharges | Total paid amount |
| InternetService | Internet service type |
| PaymentMethod | Payment method |
| Churn | Churn flag |

## Project Files

| Path | Purpose |
|---|---|
| `src/churn_analysis.py` | Clean reproducible Python script for churn metrics and baseline model |
| `requirements.txt` | Python dependencies |
| `screenshots/` | Exported visualizations |

## How to Run

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the analysis script:

```bash
python src/churn_analysis.py
```

## Methodology

The analysis follows this workflow:

1. Load customer-level data.
2. Clean missing and incorrectly typed fields.
3. Calculate overall churn rate.
4. Compare churn by contract type and payment method.
5. Build a baseline logistic regression model.
6. Evaluate the model with ROC-AUC, confusion matrix, and classification report.
7. Translate analytical findings into retention actions.

## Metrics

Churn rate:

```text
churn_rate = churned_customers / total_customers
```

Segment churn rate:

```text
segment_churn_rate = churned_customers_in_segment / total_customers_in_segment
```

Revenue exposure:

```text
monthly_revenue_exposure = sum(monthly_charges for churned customers)
```

Model quality:

```text
roc_auc = ability to rank churned customers above non-churned customers
```

## Visualizations

### Churn Distribution

![Churn Distribution](screenshots/churn_distribution.png)

### Churn by Contract Type

![Churn by Contract Type](screenshots/churn_by_contract.png)

### Monthly Charges and Churn

![Monthly Charges KDE](screenshots/monthly_charges_kde.png)

## Key Findings

1. Month-to-month contracts have higher churn than longer contracts.
2. Customers with higher monthly charges show stronger churn tendency.
3. Contract type is one of the clearest churn-related variables.
4. Tenure should be treated as a key retention dimension.
5. A baseline model gives a structured starting point for churn risk prioritization.

## Business Recommendations

1. Prioritize month-to-month customers for retention campaigns.
   They show the highest churn exposure.

2. Create offers for high-charge customers before churn risk increases.
   High monthly charges make churn more expensive for the business.

3. Encourage migration to longer contracts.
   Longer contracts are linked with stronger retention.

4. Build churn monitoring by tenure groups.
   Newer customers and short-tenure customers should be tracked separately.

5. Use churn scores for prioritization, not for automatic decisions.
   The model should support retention teams, not replace business review.

## Code Quality Improvements

The project now includes a reproducible script version of the analysis.

The script:

- separates loading, cleaning, metric calculation, modeling, and reporting into functions,
- converts `TotalCharges` safely to numeric,
- calculates churn summaries by segment,
- trains a baseline logistic regression model,
- evaluates model quality with ROC-AUC and classification metrics,
- uses clear naming and typed function signatures.

## Limitations

- The model is a baseline, not a production scoring system.
- The analysis does not include acquisition source or marketing campaign history.
- Churn causes are inferred from patterns, not proven causally.
- Revenue impact is estimated only at a high level.
- Customer lifetime value is not calculated in the current version.

## Next Steps

Planned improvements:

- add feature importance,
- create churn risk tiers,
- estimate retention campaign ROI,
- compare logistic regression with tree-based models,
- add SQL version of the analysis,
- build a Tableau dashboard for churn monitoring.

## Tools

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Jupyter Notebook
