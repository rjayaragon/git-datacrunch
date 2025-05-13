import pandas as pd
import os

WAREHOUSE_DIR = "/opt/airflow/warehouse"  # relative to project root

# Local CSV paths
customers_file = os.path.join(WAREHOUSE_DIR, "dim_customers.csv")
products_file = os.path.join(WAREHOUSE_DIR, "dim_products.csv")
sales_file = os.path.join(WAREHOUSE_DIR, "fact_sales.csv")

# Outputs
clean_path = os.path.join(WAREHOUSE_DIR, "fact_sales_clean.csv")
reject_path = os.path.join(WAREHOUSE_DIR, "fact_sales_rejected.csv")

# Load files
customers_df = pd.read_csv(customers_file)
products_df = pd.read_csv(products_file)
sales_df = pd.read_csv(sales_file)

# Filter logic
valid_customer_ids = set(customers_df["customer_id"])
valid_product_ids = set(products_df["product_id"])

is_valid_customer = sales_df["customer_id"].isin(valid_customer_ids)
is_valid_product = sales_df["product_id"].isin(valid_product_ids)

valid_sales_df = sales_df[is_valid_customer & is_valid_product]
rejected_sales_df = sales_df[~(is_valid_customer & is_valid_product)]

# Save results
valid_sales_df.to_csv(clean_path, index=False)
rejected_sales_df.to_csv(reject_path, index=False)

print(f"[✓] Cleaned sales saved: {len(valid_sales_df)} rows")
print(f"[!] Rejected sales saved: {len(rejected_sales_df)} rows")

print("Current working directory:", os.getcwd())
print("Looking for:", customers_file)
