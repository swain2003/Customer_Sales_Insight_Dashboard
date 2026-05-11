"""
generate_data.py
----------------
Generates a realistic simulated e-commerce transaction dataset (10,000+ rows).
Run this once to produce data/raw/transactions.csv before running the ETL pipeline.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# ── Reproducibility ──────────────────────────────────────────────────────────
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

# ── Config ───────────────────────────────────────────────────────────────────
NUM_RECORDS      = 12_000
NUM_CUSTOMERS    = 2_500
NUM_PRODUCTS     = 120
START_DATE       = datetime(2025, 1, 1)
END_DATE         = datetime(2026, 2, 28)

# ── Reference Data ───────────────────────────────────────────────────────────
CATEGORIES = {
    "Electronics":    {"products": ["Laptop", "Smartphone", "Tablet", "Headphones", "Smartwatch",
                                    "Camera", "Speaker", "Monitor", "Keyboard", "Mouse"],
                       "price_range": (499, 2499)},
    "Clothing":       {"products": ["T-Shirt", "Jeans", "Jacket", "Dress", "Sneakers",
                                    "Hoodie", "Shorts", "Formal Shirt", "Boots", "Cap"],
                       "price_range": (15, 249)},
    "Home & Kitchen": {"products": ["Blender", "Coffee Maker", "Air Fryer", "Vacuum", "Toaster",
                                    "Bed Sheets", "Curtains", "Lamp", "Cushion", "Cookware Set"],
                       "price_range": (25, 599)},
    "Books":          {"products": ["Fiction Novel", "Self-Help Book", "Textbook", "Comic Book",
                                    "Biography", "Cookbook", "Travel Guide", "Children's Book",
                                    "Science Book", "History Book"],
                       "price_range": (8, 89)},
    "Sports":         {"products": ["Yoga Mat", "Dumbbells", "Running Shoes", "Cycling Gloves",
                                    "Tennis Racket", "Football", "Cricket Bat", "Gym Bag",
                                    "Protein Powder", "Jump Rope"],
                       "price_range": (20, 499)},
}

PAYMENT_METHODS = ["Credit Card", "Debit Card", "UPI", "Net Banking", "Wallet", "COD"]
REGIONS         = ["North", "South", "East", "West", "Central"]

# ── Build Product Catalog ────────────────────────────────────────────────────
product_rows = []
prod_id = 1
for cat, info in CATEGORIES.items():
    for pname in info["products"]:
        lo, hi = info["price_range"]
        price   = round(random.uniform(lo, hi), 2)
        product_rows.append({"product_id": f"P{prod_id:04d}",
                              "product_name": pname,
                              "product_category": cat,
                              "unit_price": price})
        prod_id += 1

products_df = pd.DataFrame(product_rows)

# ── Generate Transactions ────────────────────────────────────────────────────
def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days),
                             hours=random.randint(0, 23),
                             minutes=random.randint(0, 59))

records = []
for i in range(1, NUM_RECORDS + 1):
    prod  = products_df.sample(1).iloc[0]
    qty   = np.random.choice([1, 1, 1, 2, 2, 3, 4, 5],
                              p=[0.35, 0.25, 0.15, 0.12, 0.06, 0.04, 0.02, 0.01])
    # inject ~3 % noise: missing values / negatives for cleaning demo
    price = prod["unit_price"] if random.random() > 0.03 else (None if random.random() > 0.5 else -1)
    qty   = qty               if random.random() > 0.02 else (None if random.random() > 0.5 else 0)

    records.append({
        "order_id":         f"ORD{i:06d}",
        "customer_id":      f"CUST{random.randint(1, NUM_CUSTOMERS):05d}",
        "product_id":       prod["product_id"],
        "product_name":     prod["product_name"],
        "product_category": prod["product_category"],
        "price":            price,
        "quantity":         qty,
        "order_date":       random_date(START_DATE, END_DATE).strftime("%Y-%m-%d %H:%M:%S"),
        "payment_method":   random.choice(PAYMENT_METHODS),
        "region":           random.choice(REGIONS),
    })

raw_df = pd.DataFrame(records)

# ── Save ─────────────────────────────────────────────────────────────────────
os.makedirs("data/raw", exist_ok=True)
raw_df.to_csv("data/raw/transactions.csv", index=False)
print(f"✅  Generated {len(raw_df):,} records → data/raw/transactions.csv")
print(raw_df.head())
