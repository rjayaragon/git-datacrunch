import psycopg2
import pandas as pd
import os
from io import StringIO

# Database connection config
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": "5434",  # Fixed from '5432'
    "dbname": "project1_db",
    "user": "admin",
    "password": "admin123",
}

# Warehouse folder path
WAREHOUSE_DIR = "/opt/airflow/warehouse"

# Tables and their corresponding files
TABLES = {
    "dim_customers": "dim_customers.csv",
    "dim_products": "dim_products.csv",
    "fact_sales": "fact_sales_clean.csv",
}


def copy_from_stringio(conn, df, table_name):
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)
    cursor = conn.cursor()
    try:
        # 🔥 THIS IS THE NEW LINE
        cursor.execute(f"TRUNCATE TABLE {table_name};")

        cursor.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV", buffer)
        conn.commit()
        print(f"[✓] Loaded {len(df)} rows into {table_name}")
    except Exception as e:
        conn.rollback()
        print(f"[!] Failed to load {table_name}: {e}")
    finally:
        cursor.close()


def main():
    print("Connecting to Postgres...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("[✓] Connected successfully.\n")
    except Exception as e:
        print(f"[!] Connection failed: {e}")
        return

    for table, filename in TABLES.items():
        filepath = os.path.join(WAREHOUSE_DIR, filename)
        if not os.path.exists(filepath):
            print(f"[!] File not found: {filepath}")
            continue
        df = pd.read_csv(filepath)
        copy_from_stringio(conn, df, table)

    conn.close()
    print("\n[✓] Data load completed.")


if __name__ == "__main__":
    main()
