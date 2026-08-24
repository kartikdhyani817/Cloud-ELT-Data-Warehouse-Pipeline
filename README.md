# Cloud-Style ELT Data Warehouse Pipeline

I'm building this project to understand how a modern **ELT and Data Warehouse pipeline** works from end to end.

Instead of jumping directly into databases and orchestration tools, I'm building the pipeline one layer at a time. The goal is to understand how raw business data is ingested, cleaned, loaded into a warehouse, transformed into analytics-ready models, tested, and eventually automated.

---

## Project Goal

The final pipeline will look roughly like this:

```text
Raw Data / API
      ↓
Python Ingestion
      ↓
PostgreSQL
      ↓
Raw Layer
      ↓
dbt
      ↓
Staging Models
      ↓
Fact + Dimension Tables
      ↓
Data Quality Tests
      ↓
Apache Airflow
      ↓
Analytics
      ↓
Dashboard
```

The project focuses on both **Data Engineering** and **Analytics Engineering** concepts.

---

## Tech Stack

The project will gradually use:

- Python
- Pandas
- SQL
- PostgreSQL
- dbt Core
- Apache Airflow
- Streamlit
- Pytest
- Git & GitHub

Everything is being built locally using free and open-source tools.

---

## Development Progress

| Day | Implementation | Status |
|---|---|---|
| Day 1 | Project Setup & Architecture | ✅ |
| Day 2 | Data Source & Python Ingestion | ✅ |
| Day 3 | PostgreSQL Raw Layer | ⏳ |
| Day 4 | Incremental Data Loading | ⏳ |
| Day 5 | dbt Setup & Staging Models | ⏳ |
| Day 6 | Fact & Dimension Tables | ⏳ |
| Day 7 | Data Quality & dbt Tests | ⏳ |
| Day 8 | Apache Airflow Orchestration | ⏳ |
| Day 9 | Logging & Pipeline Monitoring | ⏳ |
| Day 10 | Business Analytics & KPIs | ⏳ |
| Day 11 | Dashboard & Automated Testing | ⏳ |
| Day 12 | Final Integration & Documentation | ⏳ |

---

# Day 1 — Project Setup

I started by planning the overall architecture and creating a clean folder structure for the project.

The initial structure separates ingestion, SQL, dbt, Airflow, dashboard, testing, and data files so that each part of the pipeline can grow independently.

```text
Cloud_ELT_Data_Warehouse/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── ingestion/
├── sql/
├── dbt_project/
├── airflow/
├── dashboard/
├── tests/
│
├── README.md
├── requirements.txt
└── .gitignore
```

I also created the Python environment and added the initial project dependencies.

---

# Day 2 — Python Data Ingestion Pipeline

Day 2 was the first actual pipeline implementation.

I created a small retail orders dataset containing information such as:

- Order ID
- Customer ID
- Customer Name
- Product
- Category
- Quantity
- Unit Price
- Order Date
- City
- Country

The goal wasn't just to read a CSV file. I wanted to create a basic ingestion layer that checks the incoming data before it moves further into the warehouse.

---

## Current Data Flow

The pipeline currently looks like:

```text
Raw Orders CSV
      ↓
Python Ingestion
      ↓
Column Validation
      ↓
Data Cleaning
      ↓
Business Transformation
      ↓
Clean Orders CSV
      ↓
Ready for PostgreSQL
```

The next step will replace the final local-only stage with a proper PostgreSQL raw warehouse layer.

---

## Raw Data

The source dataset is stored at:

```text
data/raw/orders.csv
```

It contains retail orders from different customers, products, categories, cities, and countries.

Example structure:

```text
order_id
customer_id
customer_name
product
category
quantity
unit_price
order_date
city
country
```

---

## Python Ingestion

The ingestion logic is located in:

```text
ingestion/load_orders.py
```

The script is responsible for loading and preparing the source data.

I separated the process into different functions rather than putting everything into one block of code.

The main stages are:

```text
load_orders()
      ↓
validate_orders()
      ↓
clean_orders()
      ↓
save_clean_data()
```

This makes the ingestion process easier to understand, test, and extend later.

---

## Data Validation

Before transforming the dataset, the ingestion pipeline checks whether all required columns are available.

The expected columns include:

```text
order_id
customer_id
customer_name
product
category
quantity
unit_price
order_date
city
country
```

If one of the required columns is missing, the pipeline stops instead of silently processing an incorrect dataset.

This is a simple validation layer for now, but it gives the project a foundation for stronger data-quality checks later.

---

## Data Cleaning

After validation, the pipeline performs some basic cleaning.

This includes:

- Standardizing column names
- Removing duplicate rows
- Converting quantity to numeric
- Converting unit price to numeric
- Converting order dates to datetime
- Removing records missing important fields
- Removing orders with invalid quantities
- Removing orders with invalid prices

For example:

```text
quantity <= 0
```

or:

```text
unit_price <= 0
```

will not be included in the clean dataset.

---

## Business Transformation

I also added the first calculated business field:

```text
total_amount = quantity × unit_price
```

For example:

```text
Product     : Laptop
Quantity    : 2
Unit Price  : 75,000

Total Amount = 150,000
```

This is a small transformation, but it introduces the idea of converting raw source data into information that is more useful for analytics.

---

## Processed Data

After validation and cleaning, the output is stored in:

```text
data/processed/orders_clean.csv
```

So the current storage flow is:

```text
data/raw/orders.csv
          ↓
  Python Ingestion
          ↓
data/processed/orders_clean.csv
```

The processed dataset is now ready to be loaded into PostgreSQL.

---

## Running the Ingestion Pipeline

From the project root:

```bash
python -m ingestion.load_orders
```

A successful run should show information similar to:

```text
============================================================
Cloud ELT Data Warehouse - Order Ingestion
============================================================

Raw data loaded successfully.

Raw Rows    : 10
Required columns validated successfully.
Clean Rows  : 10
Columns     : 11
Total Sales : ...
Clean data saved to: data/processed/orders_clean.csv

Day 2 ingestion completed successfully.
```

The exact sales value depends on the source data.

---

## Current Project Structure

After Day 2:

```text
Cloud_ELT_Data_Warehouse/
│
├── data/
│   ├── raw/
│   │   └── orders.csv
│   │
│   └── processed/
│       └── orders_clean.csv
│
├── ingestion/
│   ├── __init__.py
│   └── load_orders.py
│
├── sql/
├── dbt_project/
├── airflow/
├── dashboard/
├── tests/
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## What I've Learned So Far

The project is still at an early stage, but the first two days have already covered:

- Basic ELT architecture
- Organizing a Data Engineering project
- Raw vs processed data
- CSV ingestion with Pandas
- Required-column validation
- Data type conversion
- Duplicate handling
- Basic data-quality checks
- Business transformations
- Creating reusable ingestion functions

The main thing I'm trying to avoid is treating the project as one large Python script. Each stage is being built separately so it can later become part of a larger automated pipeline.

---

## What's Next?

### Day 3 — PostgreSQL Raw Layer

The next step is to introduce the actual database layer.

The planned flow will become:

```text
orders.csv
    ↓
Python
    ↓
Cleaning / Validation
    ↓
PostgreSQL
    ↓
raw_orders
```

This will introduce:

- PostgreSQL setup
- Database connections from Python
- Warehouse schemas
- Raw tables
- SQL table creation
- Loading DataFrames into PostgreSQL

From there, the project can start moving from a simple Python ingestion script toward a proper **ELT Data Warehouse pipeline**.

---

## Project Status

**Day 2/12 completed — development in progress.**

Current milestone:

**Raw Data → Python Ingestion → Validation → Cleaning → Processed Data ✅**

Next milestone:

**Processed Data → PostgreSQL Raw Warehouse**

---

## Author

**Kartik Dhyani**

Aspiring Data Engineer interested in building practical projects around Python, SQL, ETL/ELT, data warehousing, batch processing, streaming, and modern Data Engineering tools.
