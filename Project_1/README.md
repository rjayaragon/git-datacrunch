# Project_1

## 📖 Project Overview
Project_1 is a complete end-to-end data engineering simulation. It focuses on building a modern data pipeline using Docker, PostgreSQL, and Python, following real-world best practices.

## 🛠️ Tools and Technologies
- Docker & Docker Compose
- PostgreSQL
- Python (Pandas, Faker)
- (Optional) Apache Kafka, Apache Airflow
- draw.io for architecture diagrams

## 🗂️ Project Structure
- `docker-compose.yml` to set up services
- `/scripts/` for ETL and data generation scripts
- `/models/` for schema diagrams and DDL SQL
- `/warehouse/` for cleaned data storage
- `/reports/` for SQL analytics queries

## 🚀 Current Status
- Setting up project environment (Git repository, Docker containers, initial diagrams)

---

## 📌 Next Steps
- Install Docker and Docker Compose
- Create docker-compose.yml for PostgreSQL and Airflow
- Prepare initial architecture diagrams

## Project Architecture
- Initial Architechture (P1_WK1) - Source CSVs are extracted, transformed, loaded into a Dockerized PostgreSQL warehouse for analytical querying.
![Initial ETL Architecture](models/P1_Architecture_WK1)