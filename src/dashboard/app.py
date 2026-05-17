from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Customer Sales Insights Dashboard", page_icon="📊", layout="wide")

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "processed" / "transactions_clean.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
    return df


st.title("📊 Customer Sales Insights Dashboard")
st.caption("Interactive frontend for exploring sales performance and customer behavior.")

if not DATA_PATH.exists():
    st.error("Processed data not found. Run `python src/generate_data.py` then `python src/etl/etl_pipeline.py`.")
    st.stop()

sales_df = load_data()

st.sidebar.header("Filters")
min_date = sales_df["order_date"].min().date()
max_date = sales_df["order_date"].max().date()
start_date, end_date = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

categories = sorted(sales_df["product_category"].dropna().unique())
regions = sorted(sales_df["region"].dropna().unique())
segments = sorted(sales_df["customer_segment"].dropna().unique())

selected_categories = st.sidebar.multiselect("Product Category", categories, default=categories)
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
selected_segments = st.sidebar.multiselect("Customer Segment", segments, default=segments)

mask = (
    (sales_df["order_date"].dt.date >= start_date)
    & (sales_df["order_date"].dt.date <= end_date)
    & (sales_df["product_category"].isin(selected_categories))
    & (sales_df["region"].isin(selected_regions))
    & (sales_df["customer_segment"].isin(selected_segments))
)
filtered_df = sales_df.loc[mask].copy()

if filtered_df.empty:
    st.warning("No records found for the selected filters.")
    st.stop()

avg_order_value = (
    filtered_df.groupby("order_id", as_index=False)["revenue"].sum()["revenue"].mean()
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("💰 Total Revenue", f"₹{filtered_df['revenue'].sum():,.0f}")
kpi2.metric("🛒 Total Orders", f"{filtered_df['order_id'].nunique():,}")
kpi3.metric("👤 Unique Customers", f"{filtered_df['customer_id'].nunique():,}")
kpi4.metric("📦 Avg Order Value", f"₹{avg_order_value:,.2f}")

monthly = (
    filtered_df.groupby("year_month", as_index=False)
    .agg(total_revenue=("revenue", "sum"), total_orders=("order_id", "nunique"))
    .sort_values("year_month")
)
category = (
    filtered_df.groupby("product_category", as_index=False)
    .agg(total_revenue=("revenue", "sum"))
    .sort_values("total_revenue", ascending=False)
)
products = (
    filtered_df.groupby("product_name", as_index=False)
    .agg(total_revenue=("revenue", "sum"))
    .sort_values("total_revenue", ascending=False)
    .head(10)
)
regions_df = (
    filtered_df.groupby("region", as_index=False)
    .agg(total_revenue=("revenue", "sum"))
    .sort_values("total_revenue", ascending=False)
)
segments_df = (
    filtered_df.groupby("customer_segment", as_index=False)
    .agg(total_revenue=("revenue", "sum"), customers=("customer_id", "nunique"))
    .sort_values("total_revenue", ascending=False)
)

a, b = st.columns(2)
with a:
    st.subheader("Monthly Revenue Trend")
    st.plotly_chart(
        px.line(monthly, x="year_month", y="total_revenue", markers=True),
        use_container_width=True,
    )
with b:
    st.subheader("Revenue by Product Category")
    st.plotly_chart(
        px.pie(category, values="total_revenue", names="product_category", hole=0.45),
        use_container_width=True,
    )

c, d = st.columns(2)
with c:
    st.subheader("Top 10 Products by Revenue")
    st.plotly_chart(
        px.bar(products, x="total_revenue", y="product_name", orientation="h"),
        use_container_width=True,
    )
with d:
    st.subheader("Region-wise Revenue")
    st.plotly_chart(
        px.bar(regions_df, x="region", y="total_revenue", color="region"),
        use_container_width=True,
    )

st.subheader("Customer Segment Performance")
st.plotly_chart(
    px.bar(segments_df, x="customer_segment", y="total_revenue", color="customer_segment"),
    use_container_width=True,
)

with st.expander("View Filtered Data"):
    st.dataframe(filtered_df.sort_values("order_date", ascending=False), use_container_width=True)
