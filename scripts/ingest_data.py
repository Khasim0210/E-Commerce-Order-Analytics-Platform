import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

print("✅ Connected to DB")


# =========================
# CUSTOMERS

print("Loading customers...")

customers = pd.read_csv("data/olist_customers_dataset.csv")
customers = customers.drop(columns=["customer_unique_id"])

# Skip if already loaded
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM customers"))
    count = result.scalar()

if count == 0:
    customers.to_sql("customers", engine, if_exists="append", index=False)
    print("✅ Customers loaded")
else:
    print("⏭️ Customers already loaded, skipping...")


# =========================
# PRODUCTS

products = pd.read_csv("data/olist_products_dataset.csv")

# Select only required columns (VERY IMPORTANT)
products = products[[
    "product_id",
    "product_category_name",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm"
]]

# Rename columns to match schema
products = products.rename(columns={
    "product_weight_g": "product_weight",
    "product_length_cm": "product_length",
    "product_height_cm": "product_height"
})

# Handle missing values
products = products.fillna({
    "product_category_name": "unknown",
    "product_weight": 0,
    "product_length": 0,
    "product_height": 0
})

#Skip if already loaded
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM products"))
    count = result.scalar()

if count == 0:
    products.to_sql("products", engine, if_exists="append", index=False)
    print("✅ Products loaded")
else:
    print("⏭️ Products already loaded, skipping...")


# =========================
# SELLERS

print("Loading sellers...")

sellers = pd.read_csv("data/olist_sellers_dataset.csv")

# 🔥 Skip if already loaded
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM sellers"))
    count = result.scalar()

if count == 0:
    sellers.to_sql("sellers", engine, if_exists="append", index=False)
    print("✅ Sellers loaded")
else:
    print("⏭️ Sellers already loaded, skipping...")



# =========================
# ORDERS

print("Loading orders...")

orders = pd.read_csv("data/olist_orders_dataset.csv")

# Convert date columns
date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_cols:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

# Select only required columns (match DB schema)
orders = orders[[
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_delivered_customer_date"
]]

# Rename column to match DB
orders = orders.rename(columns={
    "order_delivered_customer_date": "order_delivered_timestamp"
})

# Skip if already loaded
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM orders"))
    count = result.scalar()

if count == 0:
    orders.to_sql("orders", engine, if_exists="append", index=False)
    print("✅ Orders loaded")
else:
    print("⏭️ Orders already loaded, skipping...")


# =========================
# ORDER ITEMS

print("Loading order_items...")

order_items = pd.read_csv("data/olist_order_items_dataset.csv")

# Convert date column
order_items["shipping_limit_date"] = pd.to_datetime(
    order_items["shipping_limit_date"], errors="coerce"
)

# Select only required columns
order_items = order_items[[
    "order_id",
    "order_item_id",
    "product_id",
    "seller_id",
    "price",
    "freight_value"
]]

# Rename to match DB schema
order_items = order_items.rename(columns={
    "freight_value": "shipping_charges"
})

# Skip if already loaded
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM order_items"))
    count = result.scalar()

if count == 0:
    order_items.to_sql("order_items", engine, if_exists="append", index=False)
    print("✅ Order items loaded")
else:
    print("⏭️ Order items already loaded, skipping...")


# =========================
# PAYMENTS

print("Loading payments...")

payments = pd.read_csv("data/olist_order_payments_dataset.csv")

# Keep payment_sequential
payments = payments[[
    "order_id",
    "payment_sequential",
    "payment_type",
    "payment_installments",
    "payment_value"
]]

# Skip if already loaded
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM payments"))
    count = result.scalar()

if count == 0:
    payments.to_sql("payments", engine, if_exists="append", index=False)
    print("✅ Payments loaded")
else:
    print("⏭️ Payments already loaded, skipping...")



# =========================
# REVIEWS
# =========================

print("Loading reviews...")

reviews = pd.read_csv("data/olist_order_reviews_dataset.csv")

# Rename column
reviews = reviews.rename(columns={
    "review_comment_message": "review_comment"
})

# Select needed columns
reviews = reviews[[
    "review_id",
    "order_id",
    "review_score",
    "review_comment"
]]

# Fill nulls
reviews["review_comment"] = reviews["review_comment"].fillna("No comment")

# REMOVE DUPLICATES (THIS IS THE REAL FIX)
reviews = reviews.drop_duplicates(subset=["review_id"])

# DELETE existing data
with engine.begin() as conn:
    conn.execute(text("DELETE FROM reviews"))

# Insert clean data
reviews.to_sql("reviews", engine, if_exists="append", index=False)

print("✅ Reviews loaded (no duplicates)")