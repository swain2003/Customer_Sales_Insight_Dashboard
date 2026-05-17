<div align="center">

# 📊 Customer Sales Insights Dashboard

### End-to-End Customer Analytics, ETL & BI Dashboard System

<br>

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-success?style=for-the-badge)](https://customer-salesinsight-dashboard.streamlit.app/)

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Analytics-150458?style=for-the-badge&logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-ScientificComputing-013243?style=for-the-badge&logo=numpy)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)

![SQL](https://img.shields.io/badge/SQL-Analytics-blue?style=for-the-badge)
![ETL](https://img.shields.io/badge/ETL-Pipeline-success?style=for-the-badge)
![Data Engineering](https://img.shields.io/badge/DataEngineering-Workflow-orange?style=for-the-badge)
![Data Analytics](https://img.shields.io/badge/DataAnalytics-Insights-purple?style=for-the-badge)

![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit)
![Power BI](https://img.shields.io/badge/PowerBI-BusinessIntelligence-yellow?style=for-the-badge&logo=powerbi)
![Tableau](https://img.shields.io/badge/Tableau-Visualization-blue?style=for-the-badge&logo=tableau)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-darkgreen?style=for-the-badge)

![Seaborn](https://img.shields.io/badge/Seaborn-StatisticalCharts-4C72B0?style=for-the-badge)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter)
![Git](https://img.shields.io/badge/Git-VersionControl-F05032?style=for-the-badge&logo=git)
![GitHub](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)

</div>

---

# 🚀 Live Dashboard

🔗 **Streamlit Deployment:**  
https://customer-salesinsight-dashboard.streamlit.app/

---

# 📌 Project Overview

The **Customer Sales Insights Dashboard** is a recruiter-focused end-to-end analytics project built to simulate realistic e-commerce transaction analysis workflows using **Python**, **SQL**, **ETL pipelines**, and **Business Intelligence tools**.

The project processes and analyzes **12,000+ customer transaction records**, performs data cleaning and feature engineering, generates KPI exports for BI tools, and visualizes insights through an interactive **Streamlit dashboard**.

This project demonstrates:
- Data Engineering
- ETL Pipeline Design
- SQL Analytics
- Data Cleaning & Transformation
- Dashboard Development
- Business Intelligence Reporting

---

# ✨ Key Features

## 📊 Analytics & KPI Tracking

- Monthly Revenue Analysis
- Category-wise Sales Trends
- Regional Performance Tracking
- Top Selling Products
- Payment Method Distribution
- Customer Segmentation Analytics
- Quarterly Sales Trends
- Weekend vs Weekday Analysis

---

## 🧹 ETL Pipeline

- Duplicate record removal
- Missing value handling
- Invalid data correction
- Feature engineering
- Revenue calculation
- Customer segmentation
- Automated SQLite loading
- Processed CSV export generation

---

## 📈 Interactive Dashboard

- Streamlit-powered analytics dashboard
- KPI visualizations
- Interactive charts and metrics
- Business-ready reporting UI
- BI tool compatibility

---

# 🧰 Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Database | SQLite |
| ETL | Custom Python ETL Pipeline |
| Dashboard | Streamlit |
| Visualization | Power BI, Tableau, Matplotlib, Seaborn |
| Version Control | Git & GitHub |

---

# 📂 Project Structure

```text
customer_sales_insights/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sales_insights.db
│
├── src/
│   ├── generate_data.py
│   ├── etl/
│   │   └── etl_pipeline.py
│   ├── sql/
│   │   └── sales_queries.sql
│   ├── dashboard/
│   │   └── app.py
│   └── analysis/
│       └── run_analysis.py
│
├── dashboard_exports/
├── docs/
├── requirements.txt
└── README.md
```

---

# ⚡ Quick Start

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/customer-sales-insights.git

cd customer-sales-insights
```

---

## 2️⃣ Create & Activate Virtual Environment

### Windows (PowerShell)

```powershell
python -m venv .venv

.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python -m venv .venv

source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Generate Dataset

```bash
python src/generate_data.py
```

### Generated Output

```text
data/raw/transactions.csv
```

---

## 5️⃣ Run ETL Pipeline

```bash
python src/etl/etl_pipeline.py
```

### Generated Output

```text
data/sales_insights.db
data/processed/transactions_clean.csv
```

---

## 6️⃣ Export KPI CSVs

```bash
python src/analysis/run_analysis.py
```

### KPI Exports

```text
monthly_revenue.csv
category_sales.csv
top_products.csv
customer_segments.csv
region_performance.csv
```

These CSV exports can be directly used in:
- Power BI
- Tableau
- Excel dashboards

---

## 7️⃣ Run Interactive Dashboard

```bash
streamlit run src/dashboard/app.py
```

### Dashboard URL

```text
http://localhost:8501
```

---

# 📐 Dataset Schema

| Column | Description |
|---|---|
| order_id | Unique order identifier |
| customer_id | Unique customer identifier |
| product_id | Product SKU |
| product_name | Product display name |
| product_category | Product category |
| price | Unit price |
| quantity | Units ordered |
| revenue | Derived revenue |
| order_date | Order timestamp |
| payment_method | Payment type |
| region | Geographic region |
| customer_segment | Segmentation label |

---

# 📊 KPIs Tracked

| KPI | Description |
|---|---|
| Monthly Revenue | Revenue growth tracking |
| Category Sales | Product category analysis |
| Top Products | Best-selling products |
| Customer Segments | Customer behavior analysis |
| Payment Mix | Preferred payment methods |
| Regional Performance | Geography-based insights |
| Quarterly Trend | Quarterly growth patterns |

---

# 🧠 Resume Highlights

- Processed and analyzed **12,000+ e-commerce transaction records** using **Python, Pandas, and SQL** to uncover business insights and customer behavior patterns.
- Built an end-to-end **ETL pipeline** for automated data extraction, transformation, validation, and SQLite database loading.
- Developed KPI exports and interactive dashboards compatible with **Power BI**, **Tableau**, and **Streamlit**.
- Designed a normalized analytical database structure and optimized reporting workflows for scalable business intelligence analysis.

---

# 📈 Business Impact

✅ Automated analytics workflow  
✅ BI-ready reporting exports  
✅ Realistic customer behavior simulation  
✅ Dashboard-based decision support  
✅ Recruiter-friendly data engineering showcase  

---

# 👨‍💻 Author

## Anubhaba Swain
### B.Tech in Information Technology | KIIT University

🔗 LinkedIn:  
https://www.linkedin.com/in/anubhaba-swain-695a7b176

---

# ⭐ Support

If you found this project useful, consider giving the repository a ⭐ on GitHub.

---
