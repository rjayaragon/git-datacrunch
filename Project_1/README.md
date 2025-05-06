Project 1: Data Warehouse Pipeline – Sales Analytics
Author: RJ Aragon
Status: Week 3 Complete
Repository: datacrunch/project_1

Project Overview
This project simulates a full-stack data engineering pipeline for a fictional retail company. It demonstrates end-to-end ETL and data warehouse architecture using best practices in Python, PostgreSQL, Docker, and Airflow (planned).

The goal is to generate synthetic sales data, clean and validate it, and load it into a PostgreSQL star schema for downstream analytics and automation.

Tech Stack
Python – data generation, cleaning, validation, and loading

PostgreSQL – data warehouse (star schema)

Docker Compose – containerized Postgres DB

psycopg2 / pandas – for data I/O and transformation

Faker – for generating dummy customer, product, and sales data

Airflow (Week 4) – for pipeline orchestration (upcoming)

Directory Structure

project_1/
├── data/
│   ├── raw/                # Raw generated CSVs
│   └── cleaned/            # Cleaned data ready for load
├── warehouse/              # Backup of cleaned CSVs
├── scripts/
│   ├── generate_faker_data.py
│   ├── clean_factsales.py
│   ├── load_to_postgres.py
│   └── validate_data.py
├── models/                 # SQL DDL files
├── docker-compose.yml      # Postgres container setup
└── README.md               # This file

Week 1 – Project Setup & Architecture
Completed Tasks
Set up local development environment with Python + Docker

Created GitHub repository with clear project structure

Built initial docker-compose.yml with PostgreSQL container (port 5434)

Defined warehouse schema (star schema model)

Planned pipeline phases: generate → clean → load → validate → automate

Learnings
Learned Docker Compose basics

Practiced Git version control for DE projects

Diagrammed pipeline using draw.io

Week 2 – Data Generation & Cleaning
Completed Tasks
Generated synthetic datasets using Faker for:

Customers
Products
Sales

Cleaned issues like:

Duplicates

Nulls/missing values

Invalid email/phone formats

Inconsistent casing and spacing

📂 Cleaned Output Files
Located in data/cleaned/:

dim_customers.csv
dim_products.csv
fact_sales.csv

🛢️ Week 3 – Warehouse Load & Validation
✅ Completed Tasks
Loaded cleaned files into PostgreSQL:

dim_customers, dim_products, fact_sales_clean

Performed data validation:

Row counts

Foreign key integrity

Duplicate check

Created fact_sales_rejected.csv with invalid records

Used TRUNCATE TABLE before loading to avoid duplication

✅ Validation Summary
Metric	Result
dim_customers rows	907 ✅
dim_products rows	100 ✅
fact_sales_clean rows	4534 ✅
Missing customer_id	0 ✅
Missing product_id	0 ✅
Zero revenue/quantity	0 ✅
Duplicate order_id rows	0 ✅

🧱 Blockers & Solutions
🧩 Issue	🔍 Root Cause	🛠️ Solution
Foreign key mismatch	Cleaned customers dropped rows with invalid/missing emails, but fact_sales still referenced them	Wrote script to filter fact_sales based on valid customer_ids only
Duplicate rows in PostgreSQL	Reloads stacked data due to no truncation	Added TRUNCATE TABLE before every INSERT in load_to_postgres.py
File not found errors	Wrong directory or missing .csv extensions	Used os.path checks and consistent filenames in all scripts
Docker port conflicts	Port 5432 was already in use	Changed container port to 5434 in docker-compose.yml
Script execution errors	Running scripts from incorrect working directory	Standardized cwd and used relative paths across all scripts
Weird casing in CSV headers	Faker outputs varied cases and spacing	Cleaned columns using .str.lower().str.strip().replace() in Pandas

Week 4 Plan – Airflow & Query Layer

Goals
Automate the entire ETL flow using Airflow
Build analytical SQL queries for testing and insight extraction

Tasks
 Write analytical SQL queries (joins, KPIs, etc.)
 Save queries to /reports/query_examples.sql
 Build Airflow DAG in etl_pipeline_dag.py
 Add logging and retries in DAG tasks
 Finalize pipeline architecture diagram (with Airflow scheduling)
 Run end-to-end pipeline test:
 Faker → Extract → Clean → Load → Query

Notes
No more dim_orders — replaced by fact_sales_clean.csv
Foreign keys (customer_id, product_id) resolved before loading
Postgres exposed on localhost:5434, login admin/admin123

DAG must:
Run end-to-end on demand or scheduled
Include task retries and failure notifications (optional: email/Slack)