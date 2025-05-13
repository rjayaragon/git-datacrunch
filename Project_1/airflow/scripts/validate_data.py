import psycopg2

# Match Docker config from docker-compose and .env
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": "5434",
    "dbname": "project1_db",
    "user": "admin",
    "password": "admin123",
}


def run_validation():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("✅ Connected to Postgres\n")

        # 1. Row count check
        print("🔢 Row counts:")
        for table in ["dim_customers", "dim_products", "fact_sales"]:  # ← FIXED HERE
            cur.execute(f"SELECT COUNT(*) FROM {table};")
            count = cur.fetchone()[0]
            print(f"  - {table}: {count} rows")

        # 2. Missing foreign keys
        print("\n🔍 Foreign key integrity:")

        cur.execute(
            """
            SELECT COUNT(*) FROM fact_sales fs   -- ← FIXED HERE
            LEFT JOIN dim_customers dc ON fs.customer_id = dc.customer_id
            WHERE dc.customer_id IS NULL;
            """
        )
        print("  - Missing customer_id:", cur.fetchone()[0])

        cur.execute(
            """
            SELECT COUNT(*) FROM fact_sales fs   -- ← FIXED HERE
            LEFT JOIN dim_products dp ON fs.product_id = dp.product_id
            WHERE dp.product_id IS NULL;
            """
        )
        print("  - Missing product_id:", cur.fetchone()[0])

        # 3. Anomaly check
        print("\n⚠️ Anomalies:")

        cur.execute(
            """
            SELECT COUNT(*) FROM fact_sales     -- ← FIXED HERE
            WHERE revenue = 0 OR quantity_sold = 0;
            """
        )
        print("  - Zero revenue or quantity:", cur.fetchone()[0])

        cur.execute(
            """
            SELECT COUNT(*) FROM (
                SELECT order_id FROM fact_sales  -- ← FIXED HERE
                GROUP BY order_id HAVING COUNT(*) > 1
            ) AS duplicates;
            """
        )
        print("  - Duplicate order_id rows:", cur.fetchone()[0])

        cur.close()
        conn.close()
        print("\n✅ Validation complete!")

    except Exception as e:
        print(f"[!] Validation failed: {e}")


if __name__ == "__main__":
    run_validation()
