# 📊 Customer Sales Insights Dashboard

> End-to-end data analytics project — simulated e-commerce transaction analysis using Python, SQL, and BI tools.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![SQLite](https://img.shields.io/badge/SQLite-3.x-green?logo=sqlite)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🗂️ Project Structure

```
customer_sales_insights/
│
├── data/
│   ├── raw/                    ← Generated raw CSV (with injected noise)
│   └── processed/              ← Cleaned CSV + per-KPI export CSVs
|   └── sales_insights          ← Data Base File
├── src/
│   ├── generate_data.py        ← Simulate 12,000 e-commerce transactions
│   ├── etl/
│   │   └── etl_pipeline.py     ← Extract → Transform → Load (SQLite)
│   ├── sql/
│   │   └── sales_queries.sql   ← All analytical SQL queries
│   └── analysis/
│       └── run_analysis.py     ← Run queries → export CSVs for BI tools
│
├── dashboard_exports/          ← Screenshots / PDF exports of dashboards
├── docs/
│   └── dashboard_layout.md     ← Power BI / Tableau layout guide
├── requirements.txt
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/customer-sales-insights.git
cd customer-sales-insights
pip install -r requirements.txt
```

### 2. Generate Dataset

```bash
python src/generate_data.py
# → data/raw/transactions.csv  (12,000 rows)
```

### 3. Run ETL Pipeline

```bash
python src/etl/etl_pipeline.py
# → data/sales_insights.db      (SQLite)
# → data/processed/transactions_clean.csv
```

### 4. Export KPI CSVs (for Power BI / Tableau)

```bash
python src/analysis/run_analysis.py
# → data/processed/monthly_revenue.csv
# → data/processed/category_sales.csv
# → data/processed/top_products.csv
# → ...and more
```

### 5. Connect BI Tool

**Power BI**: Home → Get Data → Text/CSV → select any file in `data/processed/`  
**Tableau**: Connect → To a File → Text File → select CSV

---

## 📐 Dataset Schema

| Column             | Type    | Description                           |
|--------------------|---------|---------------------------------------|
| order_id           | TEXT    | Unique order identifier               |
| customer_id        | TEXT    | Unique customer identifier            |
| product_id         | TEXT    | Product SKU                           |
| product_name       | TEXT    | Product display name                  |
| product_category   | TEXT    | Electronics / Clothing / etc.         |
| price              | REAL    | Unit price (INR)                      |
| quantity           | INT     | Units ordered                         |
| revenue            | REAL    | price × quantity (derived)            |
| order_date         | DATETIME| Order timestamp                       |
| year / month       | INT     | Extracted time features               |
| year_month         | TEXT    | Period string e.g. "2025-03"          |
| quarter            | INT     | 1–4                                   |
| day_of_week        | TEXT    | Monday … Sunday                       |
| is_weekend         | BOOL    | 1 if Sat/Sun                          |
| payment_method     | TEXT    | Credit Card / UPI / COD / etc.        |
| region             | TEXT    | North / South / East / West / Central |
| customer_segment   | TEXT    | One-Time / Occasional / Regular / Loyal|

---

## 📊 KPIs Tracked

| KPI                     | Source Query              |
|-------------------------|---------------------------|
| Monthly Revenue         | `monthly_revenue`         |
| Category-wise Sales     | `category_sales`          |
| Top Products            | `top_products`            |
| Customer Segments       | `customer_segments`       |
| Payment Method Mix      | `payment_methods`         |
| Regional Performance    | `region_performance`      |
| Quarterly Trend         | `quarterly_trend`         |
| Weekend vs Weekday      | `day_type_sales`          |

---

## 🛠️ Tech Stack

| Layer       | Tool / Library                  |
|-------------|---------------------------------|
| Language    | Python 3.10+                    |
| Data Wrangling | Pandas, NumPy                |
| Database    | SQLite 3 (via `sqlite3`)        |
| ETL         | Custom Python pipeline          |
| BI / Viz    | Power BI Desktop / Tableau Public|
| Version Control | Git + GitHub               |

---

## 🧹 ETL Pipeline — What It Does

```
RAW CSV (noisy)
    ↓  Extract
DataFrame in memory
    ↓  Transform
      • Drop duplicates
      • Impute invalid price (median)
      • Fix invalid quantity (floor = 1)
      • Remove future-dated records
      • Normalize string columns
      • Engineer: revenue, year/month/quarter/week, is_weekend, customer_segment
    ↓  Load
      • SQLite: transactions + dim_product + dim_customer + indexes
      • Processed CSV
```

---

## 📋 Resume Bullet Points (what this project demonstrates)

- Analyzed **12,000+** e-commerce transactions using **Python (Pandas)** and **SQL** to uncover sales trends and customer purchasing behavior across **5+ product categories**.
- Built an **ETL pipeline** ensuring **100% data consistency** — handling missing values, invalid records, and duplicate orders.
- Engineered KPI exports (monthly revenue, category-wise sales, top products) ready for **Power BI / Tableau** dashboards.
- Designed a **normalized SQLite schema** with dimension tables and indexes for fast analytical queries.

---

## 📄 License

MIT © 2026
