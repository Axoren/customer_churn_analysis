# Customer Churn Analysis

This project analyzes customer churn behavior based on the Telco dataset.

📁 Dataset: `WA_Fn-UseC_-Telco-Customer-Churn.csv`  
📅 Project Date: June 8, 2022  
📌 Tools: `Pandas`, `Matplotlib`, `Seaborn`, `Jupyter Notebook`

## 📌 Objective

The goal is to identify factors that contribute to customer churn and visualize the relationship between churn and key variables such as contract type, monthly charges, and service usage.

## 🔍 Key Findings

- **Churn Rate Distribution**  
  The dataset shows a higher churn rate among month-to-month contracts.
  ![Churn Distribution](screenshots/churn_distribution.png)

- **Churn Rate by Contract Type**  
  Customers with longer contracts tend to stay longer.
  ![Churn by Contract Type](screenshots/churn_by_contract.png)

- **Monthly Charges and Churn**  
  Customers with higher monthly charges are more likely to churn.
  ![Monthly Charges KDE](screenshots/monthly_charges_kde.png)

## 📊 Tools and Techniques

- **EDA** with Pandas and Seaborn
- **Data cleaning** and formatting
- **Churn rate calculation**
- **Distribution & KDE plots**
