"""
etl_pipeline.py
---------------
Full Extract → Transform → Load pipeline.

  Extract  : Read raw CSV from data/raw/
  Transform: Clean, validate, enrich with derived columns
  Load     : Persist clean data to SQLite (data/sales_insights.db)
             AND export CSV to data/processed/

Usage:
    python src/etl/etl_pipeline.py
"""

import pandas as pd
import numpy as np
import sqlite3
import os
import logging
from pathlib import Path
from datetime import datetime

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("ETL")

# Paths
BASE_DIR      = Path(__file__).resolve().parents[2]
RAW_CSV       = BASE_DIR / "data" / "raw"       / "transactions.csv"
PROCESSED_CSV = BASE_DIR / "data" / "processed" / "transactions_clean.csv"
DB_PATH       = BASE_DIR / "data"               / "sales_insights.db"

# EXTRACT
def extract(path: Path) -> pd.DataFrame:
    log.info(f"[EXTRACT] Reading → {path}")
    df = pd.read_csv(path, parse_dates=["order_date"])
    log.info(f"[EXTRACT] Loaded {len(df):,} rows × {df.shape[1]} cols")
    return df

#TRANSFORM
def transform(df: pd.DataFrame) -> pd.DataFrame:
    log.info("[TRANSFORM] Starting cleaning & feature engineering …")
    original_len = len(df)

    # 1. Drop full duplicates
    df.drop_duplicates(subset=["order_id"], inplace=True)
    log.info(f"  → Dropped {original_len - len(df)} duplicate rows")

    # 2. Handle missing / invalid price
    bad_price = df["price"].isna() | (df["price"] <= 0)
    median_price = df.loc[~bad_price, "price"].median()
    df.loc[bad_price, "price"] = median_price
    log.info(f"  → Imputed {bad_price.sum()} bad price values with median ({median_price:.2f})")

    # 3. Handle missing / invalid quantity
    bad_qty = df["quantity"].isna() | (df["quantity"] <= 0)
    df.loc[bad_qty, "quantity"] = 1        # sensible floor
    df["quantity"] = df["quantity"].astype(int)
    log.info(f"  → Fixed {bad_qty.sum()} bad quantity values → 1")

    # 4. Ensure order_date is datetime
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    future_mask = df["order_date"] > datetime.now()
    df.loc[future_mask, "order_date"] = pd.NaT
    df.dropna(subset=["order_date"], inplace=True)

    # 5. Normalise string columns
    for col in ["product_category", "payment_method", "region"]:
        df[col] = df[col].str.strip().str.title()

    # 6. Feature engineering ─ derived columns
    df["revenue"]       = (df["price"] * df["quantity"]).round(2)
    df["year"]          = df["order_date"].dt.year
    df["month"]         = df["order_date"].dt.month
    df["month_name"]    = df["order_date"].dt.strftime("%b")
    df["quarter"]       = df["order_date"].dt.quarter
    df["week"]          = df["order_date"].dt.isocalendar().week.astype(int)
    df["day_of_week"]   = df["order_date"].dt.day_name()
    df["is_weekend"]    = df["order_date"].dt.dayofweek >= 5

    df["year_month"]    = df["order_date"].dt.to_period("M").astype(str)   # e.g. "2025-03"

    # 7. Customer segment (RFM-lite: order frequency proxy)
    order_freq = df.groupby("customer_id")["order_id"].transform("count")
    df["customer_segment"] = pd.cut(order_freq,
                                    bins=[0, 2, 5, 10, np.inf],
                                    labels=["One-Time", "Occasional", "Regular", "Loyal"])

    log.info(f"[TRANSFORM] Done. Clean rows: {len(df):,}")
    return df

# LOAD
def load_to_csv(df: pd.DataFrame, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    log.info(f"[LOAD] CSV → {path}  ({len(df):,} rows)")


def load_to_sqlite(df: pd.DataFrame, db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur  = conn.cursor()

    #DDL
    cur.executescript("""
        PRAGMA journal_mode=WAL;

        CREATE TABLE IF NOT EXISTS transactions (
            order_id          TEXT PRIMARY KEY,
            customer_id       TEXT NOT NULL,
            product_id        TEXT NOT NULL,
            product_name      TEXT NOT NULL,
            product_category  TEXT NOT NULL,
            price             REAL NOT NULL,
            quantity          INTEGER NOT NULL,
            revenue           REAL NOT NULL,
            order_date        TEXT NOT NULL,
            year              INTEGER,
            month             INTEGER,
            month_name        TEXT,
            quarter           INTEGER,
            week              INTEGER,
            day_of_week       TEXT,
            is_weekend        INTEGER,
            year_month        TEXT,
            payment_method    TEXT,
            region            TEXT,
            customer_segment  TEXT
        );

        CREATE TABLE IF NOT EXISTS dim_product (
            product_id       TEXT PRIMARY KEY,
            product_name     TEXT NOT NULL,
            product_category TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS dim_customer (
            customer_id       TEXT PRIMARY KEY,
            customer_segment  TEXT
        );
    """)

    #Upsert transactions
    cols = ["order_id","customer_id","product_id","product_name","product_category",
            "price","quantity","revenue","order_date","year","month","month_name",
            "quarter","week","day_of_week","is_weekend","year_month",
            "payment_method","region","customer_segment"]
    df[cols].to_sql("transactions", conn, if_exists="replace", index=False)
    log.info(f"  → Loaded {len(df):,} rows into [transactions]")

    #Dimension tables
    (df[["product_id","product_name","product_category"]]
       .drop_duplicates()
       .to_sql("dim_product", conn, if_exists="replace", index=False))

    (df[["customer_id","customer_segment"]]
       .drop_duplicates(subset=["customer_id"])
       .to_sql("dim_customer", conn, if_exists="replace", index=False))

    #Indexes for query performance
    cur.executescript("""
        CREATE INDEX IF NOT EXISTS idx_txn_date     ON transactions(order_date);
        CREATE INDEX IF NOT EXISTS idx_txn_category ON transactions(product_category);
        CREATE INDEX IF NOT EXISTS idx_txn_customer ON transactions(customer_id);
        CREATE INDEX IF NOT EXISTS idx_txn_ym       ON transactions(year_month);
    """)

    conn.commit()
    conn.close()
    log.info(f"[LOAD] SQLite → {db_path}")


# PIPELINE ENTRY POINT
def run_pipeline():
    log.info("=" * 60)
    log.info("  CUSTOMER SALES INSIGHTS — ETL PIPELINE")
    log.info("=" * 60)

    raw_df   = extract(RAW_CSV)
    clean_df = transform(raw_df)
    load_to_csv(clean_df, PROCESSED_CSV)
    load_to_sqlite(clean_df, DB_PATH)

    log.info("=" * 60)
    log.info("  ✅  Pipeline complete!")
    log.info("=" * 60)
    return clean_df


if __name__ == "__main__":
    run_pipeline()
