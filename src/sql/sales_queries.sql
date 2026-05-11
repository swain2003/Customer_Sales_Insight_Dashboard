-- =============================================================
-- sales_queries.sql
-- Customer Sales Insights — Analytical SQL Queries
-- Compatible with: SQLite 3.x  |  PostgreSQL 13+
-- =============================================================


-- ┌─────────────────────────────────────────────────────────────┐
-- │  1. MONTHLY REVENUE                                         │
-- └─────────────────────────────────────────────────────────────┘
-- Total revenue, order count, and avg order value per month
SELECT
    year_month,
    year,
    month,
    month_name,
    COUNT(DISTINCT order_id)      AS total_orders,
    COUNT(DISTINCT customer_id)   AS unique_customers,
    ROUND(SUM(revenue), 2)        AS total_revenue,
    ROUND(AVG(revenue), 2)        AS avg_order_value,
    ROUND(SUM(quantity), 0)       AS units_sold
FROM transactions
GROUP BY year_month, year, month, month_name
ORDER BY year, month;


-- ┌─────────────────────────────────────────────────────────────┐
-- │  2. CATEGORY-WISE SALES PERFORMANCE                         │
-- └─────────────────────────────────────────────────────────────┘
SELECT
    product_category,
    COUNT(DISTINCT order_id)                                   AS orders,
    SUM(quantity)                                              AS units_sold,
    ROUND(SUM(revenue), 2)                                     AS total_revenue,
    ROUND(AVG(revenue), 2)                                     AS avg_revenue_per_order,
    ROUND(SUM(revenue) * 100.0 /
          SUM(SUM(revenue)) OVER (), 2)                        AS revenue_share_pct
FROM transactions
GROUP BY product_category
ORDER BY total_revenue DESC;


-- ┌─────────────────────────────────────────────────────────────┐
-- │  3. TOP 10 PRODUCTS BY REVENUE                              │
-- └─────────────────────────────────────────────────────────────┘
SELECT
    product_id,
    product_name,
    product_category,
    COUNT(DISTINCT order_id)  AS times_ordered,
    SUM(quantity)             AS units_sold,
    ROUND(SUM(revenue), 2)   AS total_revenue,
    ROUND(AVG(price), 2)     AS avg_price
FROM transactions
GROUP BY product_id, product_name, product_category
ORDER BY total_revenue DESC
LIMIT 10;


-- ┌─────────────────────────────────────────────────────────────┐
-- │  4. CUSTOMER PURCHASING BEHAVIOUR                           │
-- └─────────────────────────────────────────────────────────────┘

-- 4a. Segment distribution
SELECT
    customer_segment,
    COUNT(DISTINCT customer_id)  AS customer_count,
    ROUND(SUM(revenue), 2)       AS segment_revenue,
    ROUND(AVG(revenue), 2)       AS avg_order_value
FROM transactions
GROUP BY customer_segment
ORDER BY segment_revenue DESC;

-- 4b. Top 20 customers by lifetime value
SELECT
    customer_id,
    customer_segment,
    COUNT(DISTINCT order_id)   AS total_orders,
    SUM(quantity)              AS total_units,
    ROUND(SUM(revenue), 2)    AS lifetime_value,
    MIN(order_date)            AS first_order,
    MAX(order_date)            AS last_order
FROM transactions
GROUP BY customer_id, customer_segment
ORDER BY lifetime_value DESC
LIMIT 20;

-- 4c. Payment method breakdown
SELECT
    payment_method,
    COUNT(*)                    AS transactions,
    ROUND(SUM(revenue), 2)     AS total_revenue,
    ROUND(AVG(revenue), 2)     AS avg_order_value,
    ROUND(COUNT(*) * 100.0 /
          (SELECT COUNT(*) FROM transactions), 2) AS usage_pct
FROM transactions
GROUP BY payment_method
ORDER BY transactions DESC;


-- ┌─────────────────────────────────────────────────────────────┐
-- │  5. REGION-WISE PERFORMANCE                                 │
-- └─────────────────────────────────────────────────────────────┘
SELECT
    region,
    COUNT(DISTINCT customer_id)  AS customers,
    COUNT(DISTINCT order_id)     AS orders,
    ROUND(SUM(revenue), 2)       AS total_revenue,
    ROUND(AVG(revenue), 2)       AS avg_order_value
FROM transactions
GROUP BY region
ORDER BY total_revenue DESC;


-- ┌─────────────────────────────────────────────────────────────┐
-- │  6. WEEKEND vs WEEKDAY SALES                                │
-- └─────────────────────────────────────────────────────────────┘
SELECT
    CASE WHEN is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS day_type,
    COUNT(DISTINCT order_id)    AS orders,
    ROUND(SUM(revenue), 2)      AS total_revenue,
    ROUND(AVG(revenue), 2)      AS avg_order_value
FROM transactions
GROUP BY is_weekend;


-- ┌─────────────────────────────────────────────────────────────┐
-- │  7. QUARTERLY REVENUE TREND                                 │
-- └─────────────────────────────────────────────────────────────┘
SELECT
    year,
    quarter,
    year || '-Q' || quarter                  AS year_quarter,
    ROUND(SUM(revenue), 2)                   AS quarterly_revenue,
    COUNT(DISTINCT order_id)                 AS total_orders,
    ROUND(SUM(revenue) - LAG(SUM(revenue))
          OVER (ORDER BY year, quarter), 2)  AS revenue_change_qoq
FROM transactions
GROUP BY year, quarter
ORDER BY year, quarter;


-- ┌─────────────────────────────────────────────────────────────┐
-- │  8. PRODUCT CATEGORY × REGION HEATMAP                      │
-- └─────────────────────────────────────────────────────────────┘
SELECT
    product_category,
    region,
    ROUND(SUM(revenue), 2) AS revenue
FROM transactions
GROUP BY product_category, region
ORDER BY product_category, revenue DESC;
