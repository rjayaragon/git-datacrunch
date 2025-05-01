import pandas as pd
import os
import logging

# folder to get the raw data
data_folder = "data"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logging.info("Loading customers.csv")
customers_df = pd.read_csv(os.path.join(data_folder, "customers.csv"))
logging.info(f"Loaded customers.csv with shape: {customers_df.shape}")

logging.info("Loading orders.csv")
orders_df = pd.read_csv(os.path.join(data_folder, "orders.csv"))
logging.info(f"Loading orders.csv with shape: {orders_df.shape}")

logging.info("Loading products.csv")
products_df = pd.read_csv(os.path.join(data_folder, "products.csv"))
logging.info(f"Loading products.csv with shape: {products_df.shape}")

logging.info("Loading sales.csv")
sales_df = pd.read_csv(os.path.join(data_folder, "sales.csv"))
logging.info(f"Loading sales.csv with shape: {sales_df.shape}")

# inspect file
print("Customers Schema:")
print(customers_df.dtypes)
print("Orders Schema:")
print(orders_df.dtypes)
print("Products Schema:")
print(products_df.dtypes)
print("Sales Schema:")
print(sales_df.dtypes)

print("\nExtraction Successful!")

# cleaning

print("\ncleaned_customers.csv")

# drop rows with missing email
customers_df = customers_df.dropna(subset=["email"])

# keep only email containing '@' AND '.'
customers_df = customers_df[customers_df["email"].str.contains("@", na=False)]
customers_df = customers_df[customers_df["email"].str.contains(".", na=False)]

# remove leading titles in email
customers_df["email"] = customers_df["email"].str.replace(
    r"(mr\.|ms\.|mrs\.|dr\.)", "", case=False, regex=True
)

# remove double dots '..'
customers_df["email"] = customers_df["email"].str.replace(r"\.\.", ".", regex=True)

# remove trailing titles in email
customers_df["email"] = customers_df["email"].str.replace(
    r"\.?(jr|md|dvm|dds)\b", "", regex=True
)

# remove stray for directly after the @ sign
customers_df["email"] = customers_df["email"].str.replace(r"\.@", "@", regex=True)

# correct @exampl.com to @example.com
customers_df["email"] = customers_df["email"].str.replace(
    "exampl.com", "example.com", regex=False
)

# remove trailing '.' in email column
customers_df["email"] = customers_df["email"].str.lstrip(".")


logging.info("Removing titles from customer names (prefixes and suffixes)...")
# remove titles in column name and keep person's real name (leading)
customers_df["name"] = customers_df["name"].str.replace(
    r"^(Mr\.|Ms\.|Mrs\.|Dr\.)\s+", "", regex=True
)

# remove titles in column name and keep person's real name (trailing)
customers_df["name"] = customers_df["name"].str.replace(
    r"\s+(MD|DDS|Jr\.?|DVM)$", "", regex=True
)

# fix sign up date
customers_df["signup_date"] = pd.to_datetime(
    customers_df["signup_date"], errors="coerce"
)

# orders cleaning
print("\ncleaned_orders.csv")

# fix order_date format
orders_df["order_date"] = pd.to_datetime(orders_df["order_date"], errors="coerce")

logging.info("Corrected spelling under category_column.")
print("\ncleaned_products.csv")
# fix common typos
products_df["category"] = products_df["category"].replace(
    {"Clothng": "Clothing", "Sprots": "Sports", "Hme": "Home"}
)

logging.info("Updated 0.00 value to $5 for min purchases.")
# set 0.0 product price to minimum $5
products_df["product_price"] = products_df["product_price"].apply(
    lambda x: 5 if x == 0 else x
)

logging.info("No changes made on this file for now.")
# nothing to clean for now
print("\ncleaned_sales.csv")

warehouse = "warehouse"
os.makedirs(warehouse, exist_ok=True)

customers_df.to_csv(os.path.join(warehouse, "dim_customers.csv"), index=False)
orders_df.to_csv(os.path.join(warehouse, "dim_orders.csv"), index=False)
products_df.to_csv(os.path.join(warehouse, "dim_products.csv"), index=False)
sales_df.to_csv(os.path.join(warehouse, "star_sales.csv"), index=False)

logging.info("Saving cleaned data to warehouse/ as dimension and fact tables...")
logging.info("Data pipeline completed successfully.")
logging.info("Customers Schema:\n" + str(customers_df.dtypes))
