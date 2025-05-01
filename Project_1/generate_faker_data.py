import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import os

fake = Faker()

# Create output folder
output_folder = "data"
os.makedirs(output_folder, exist_ok=True)

# ----------------------------
# 1. Generate customers.csv (refined to match name and email)
# ----------------------------
customers = []
for i in range(1, 1001):
    name = fake.name()

    # Create messy emails
    if random.random() > 0.05:
        email_name = name.lower().replace(" ", ".")
        if random.random() > 0.1:
            email = f"{email_name}@example.com"
        else:
            # 10% bad emails (missing '@' or typo domain)
            email = (
                f"{email_name}example.com"
                if random.random() < 0.5
                else f"{email_name}@exampl.com"
            )
    else:
        email = None  # 5% missing emails

    location = fake.city() if random.random() > 0.1 else "Unknown"  # 10% bad locations
    signup_date = fake.date_between(start_date="-5y", end_date="today")

    customers.append([i, name, email, location, signup_date])

customers_df = pd.DataFrame(
    customers, columns=["customer_id", "name", "email", "location", "signup_date"]
)
customers_df.to_csv(f"{output_folder}/customers.csv", index=False)

# ----------------------------
# 2. Generate products.csv
# ----------------------------
categories = ["Electronics", "Clothing", "Home", "Beauty", "Sports", "Books", "Toys"]

products = []
for i in range(1, 101):
    category = random.choice(
        categories + ["Clothng", "Sprots", "Hme"]
    )  # Add some typos
    price = (
        round(random.uniform(5, 500), 2) if random.random() > 0.02 else 0.0
    )  # 2% free products
    products.append([i, fake.word().capitalize(), category, price])

products_df = pd.DataFrame(
    products, columns=["product_id", "product_name", "category", "product_price"]
)
products_df.to_csv(f"{output_folder}/products.csv", index=False)

# ----------------------------
# 3. Generate orders.csv
# ----------------------------
orders = []
for i in range(1, 5001):
    customer_id = random.randint(1, 1000)
    product_id = random.randint(1, 100)
    amount = round(random.uniform(10, 1000), 2)
    if random.random() < 0.02:
        amount = round(random.uniform(-100, -10), 2)  # 2% negative amounts (messy)
    order_date = fake.date_between(start_date="-3y", end_date="today")
    orders.append([i, customer_id, product_id, amount, order_date])

orders_df = pd.DataFrame(
    orders, columns=["order_id", "customer_id", "product_id", "amount", "order_date"]
)
orders_df.to_csv(f"{output_folder}/orders.csv", index=False)

# ----------------------------
# 4. Generate sales.csv
# ----------------------------
sales = []
for i in range(1, 5001):
    quantity_sold = random.randint(1, 5)
    revenue = round(quantity_sold * random.uniform(10, 200), 2)
    if random.random() < 0.03:
        revenue = round(revenue * random.uniform(1.5, 2.0), 2)  # 3% unrealistic revenue
    sales.append([i, quantity_sold, revenue])

sales_df = pd.DataFrame(sales, columns=["order_id", "quantity_sold", "revenue"])
sales_df.to_csv(f"{output_folder}/sales.csv", index=False)

print("✅ Fake datasets generated successfully!")
