# Dashboard Layout Guide — Power BI / Tableau
## Customer Sales Insights Dashboard

---

## Page 1 — Executive Overview

**Purpose**: Single-glance summary for stakeholders.

### KPI Cards (top row — 4 cards)
| Card | Metric | Format |
|------|--------|--------|
| 💰 Total Revenue | SUM(revenue) | ₹ 1.23 Cr |
| 🛒 Total Orders | COUNT(order_id) | 12,000 |
| 👤 Unique Customers | COUNT DISTINCT(customer_id) | 2,500 |
| 📦 Avg Order Value | AVG(revenue) | ₹ 456 |

### Charts (main area)
1. **Line Chart** — Monthly Revenue Trend (Jan 2025 – Feb 2026)
   - X-axis: year_month | Y-axis: total_revenue | Color: quarterly bands
2. **Donut Chart** — Revenue by Product Category (5 segments)
3. **Bar Chart** — Top 10 Products by Revenue (horizontal bars)
4. **Map / Filled Map** — Region-wise Revenue (5 regions, color intensity = revenue)

### Filters (right panel)
- Date Range Slicer (year_month)
- Product Category (multi-select)
- Region (multi-select)
- Customer Segment (multi-select)

---

## Page 2 — Sales Deep Dive

1. **Stacked Column Chart** — Monthly Revenue by Category
2. **Scatter Plot** — Avg Price vs Units Sold (by product, sized by revenue)
3. **Matrix / Heatmap** — Category × Region Revenue
4. **100% Stacked Bar** — Payment Method Mix by Month

---

## Page 3 — Customer Behaviour

1. **Funnel Chart** — Customer Segment (Loyal → Regular → Occasional → One-Time)
2. **Bar Chart** — Top 20 Customers by Lifetime Value
3. **Pie / Donut** — Weekend vs Weekday Orders
4. **Line Chart** — Daily Order Volume (7-day rolling average)

---

## Power BI Setup Steps

1. Open Power BI Desktop → **Get Data** → **Text/CSV**
2. Import each file from `data/processed/`:
   - `transactions_clean.csv` (main fact table)
   - `monthly_revenue.csv`
   - `category_sales.csv`
   - `top_products.csv`
3. Create relationships: `transactions_clean[product_id]` → `top_products[product_id]`
4. Create measures:
   ```
   Total Revenue = SUM(transactions_clean[revenue])
   Avg Order Value = AVERAGE(transactions_clean[revenue])
   MoM Growth % = 
       VAR current = [Total Revenue]
       VAR prev = CALCULATE([Total Revenue], DATEADD(transactions_clean[order_date], -1, MONTH))
       RETURN DIVIDE(current - prev, prev) * 100
   ```

## Tableau Setup Steps

1. Connect → To a File → **Text File** → `transactions_clean.csv`
2. Drag `order_date` to Columns (set to Month), `revenue` to Rows → Line chart
3. Use **Show Me** panel to switch chart types
4. Add filters via the Filters shelf (product_category, region, customer_segment)
5. Publish to Tableau Public for free hosting

---

## Color Palette Recommendation

| Color | Hex | Use |
|-------|-----|-----|
| Deep Navy | `#1B2A4A` | Background / headers |
| Electric Blue | `#2563EB` | Primary metric / lines |
| Amber | `#F59E0B` | Highlight / alerts |
| Emerald | `#10B981` | Positive trend |
| Rose | `#F43F5E` | Negative / decline |
| Slate | `#64748B` | Secondary text |
