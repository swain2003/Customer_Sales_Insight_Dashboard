"""
run_analysis.py
---------------
Runs all analytical SQL queries against the SQLite database and
saves each result as a CSV in data/processed/ for Power BI / Tableau import.
"""

import sqlite3
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger("Analysis")

BASE_DIR  = Path(__file__).resolve().parents[2]
DB_PATH   = BASE_DIR / "data" / "sales_insights.db"
OUT_DIR   = BASE_DIR / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

QUERIES = {
    "monthly_revenue": """
        SELECT year_month, year, month, month_name,
               COUNT(DISTINCT order_id) AS total_orders,
               COUNT(DISTINCT customer_id) AS unique_customers,
               ROUND(SUM(revenue),2) AS total_revenue,
               ROUND(AVG(revenue),2) AS avg_order_value,
               SUM(quantity) AS units_sold
        FROM transactions
        GROUP BY year_month, year, month, month_name
        ORDER BY year, month
    """,
    "category_sales": """
        SELECT product_category,
               COUNT(DISTINCT order_id) AS orders,
               SUM(quantity) AS units_sold,
               ROUND(SUM(revenue),2) AS total_revenue,
               ROUND(AVG(revenue),2) AS avg_order_value,
               ROUND(SUM(revenue)*100.0/SUM(SUM(revenue)) OVER(),2) AS revenue_share_pct
        FROM transactions
        GROUP BY product_category
        ORDER BY total_revenue DESC
    """,
    "top_products": """
        SELECT product_id, product_name, product_category,
               COUNT(DISTINCT order_id) AS times_ordered,
               SUM(quantity) AS units_sold,
               ROUND(SUM(revenue),2) AS total_revenue,
               ROUND(AVG(price),2) AS avg_price
        FROM transactions
        GROUP BY product_id, product_name, product_category
        ORDER BY total_revenue DESC
        LIMIT 20
    """,
    "customer_segments": """
        SELECT customer_segment,
               COUNT(DISTINCT customer_id) AS customer_count,
               ROUND(SUM(revenue),2) AS segment_revenue,
               ROUND(AVG(revenue),2) AS avg_order_value
        FROM transactions
        GROUP BY customer_segment
        ORDER BY segment_revenue DESC
    """,
    "payment_methods": """
        SELECT payment_method,
               COUNT(*) AS transactions,
               ROUND(SUM(revenue),2) AS total_revenue,
               ROUND(AVG(revenue),2) AS avg_order_value,
               ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM transactions),2) AS usage_pct
        FROM transactions
        GROUP BY payment_method
        ORDER BY transactions DESC
    """,
    "region_performance": """
        SELECT region,
               COUNT(DISTINCT customer_id) AS customers,
               COUNT(DISTINCT order_id) AS orders,
               ROUND(SUM(revenue),2) AS total_revenue,
               ROUND(AVG(revenue),2) AS avg_order_value
        FROM transactions
        GROUP BY region
        ORDER BY total_revenue DESC
    """,
    "quarterly_trend": """
        SELECT year, quarter,
               year||'-Q'||quarter AS year_quarter,
               ROUND(SUM(revenue),2) AS quarterly_revenue,
               COUNT(DISTINCT order_id) AS total_orders
        FROM transactions
        GROUP BY year, quarter
        ORDER BY year, quarter
    """,
    "day_type_sales": """
        SELECT CASE WHEN is_weekend=1 THEN 'Weekend' ELSE 'Weekday' END AS day_type,
               COUNT(DISTINCT order_id) AS orders,
               ROUND(SUM(revenue),2) AS total_revenue,
               ROUND(AVG(revenue),2) AS avg_order_value
        FROM transactions GROUP BY is_weekend
    """,
}


def run_all():
    conn = sqlite3.connect(DB_PATH)
    for name, sql in QUERIES.items():
        df = pd.read_sql_query(sql, conn)
        out = OUT_DIR / f"{name}.csv"
        df.to_csv(out, index=False)
        log.info(f"  ✅  {name:<25}  {len(df):>5} rows  → {out.name}")
    conn.close()
    log.info("All exports complete.")


if __name__ == "__main__":
    run_all()
