# Cloud-Style ELT Data Warehouse Pipelinek

I'm building this project to understand how a real-world **Data Engineering pipeline** is designed and how raw business data moves from a source system into an analytics-ready warehouse.

I'm developing it step by step instead of trying to build everything at once. The idea is to understand each layer properly — ingestion, storage, transformation, testing, and eventually orchestration.

The project is currently being built locally using free tools.

---

## Project Goal

The final pipeline is planned to look like this:

```text
Raw Data / API
      ↓
Python Ingestion
      ↓
Data Validation & Cleaning
      ↓
MySQL
      ↓
Raw Warehouse Layer
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

The project combines **Data Engineering** and **Analytics Engineering** concepts.

---

## Tech Stack

The project will gradually use:

- Python
- Pandas
- SQL
- MySQL
- dbt Core
- Apache Airflow
- Streamlit
- Pytest
- Git
- GitHub

The tools are being used locally with a focus on free and open-source technologies.

---

# Development Progress

| Day | Work Completed | Status |
|---|---|---|
| Day 1 | Project Setup & Architecture | ✅ |
| Day 2 | Python Data Ingestion Pipeline | ✅ |
| Day 3 | MySQL Raw Warehouse Layer | ✅ |
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

The first day was mainly about planning the project and creating a structure that could support the complete pipeline later.

I separated the project into different areas for:

- Data
- Python ingestion
- SQL
- dbt
- Airflow
- Dashboard
- Testing

The initial structure was:

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

I also created the initial GitHub repository and project configuration.

---

# Day 2 — Python Data Ingestion

On Day 2, I started building the actual pipeline.

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

The raw dataset is stored in:

```text
data/raw/orders.csv
```

---

## Data Ingestion Flow

The Python ingestion process currently works like this:

```text
orders.csv
    ↓
Load Data
    ↓
Validate Columns
    ↓
Clean Data
    ↓
Remove Duplicates
    ↓
Convert Data Types
    ↓
Calculate Total Amount
    ↓
orders_clean.csv
```

The main ingestion script is:

```text
ingestion/load_orders.py
```

---

## Validation

Before processing the data, the script checks that the required columns exist.

It also handles:

- Duplicate rows
- Invalid quantities
- Invalid prices
- Missing important fields
- Date conversion
- Numeric conversion

This prevents obviously invalid data from entering the next stage.

---

## Business Transformation

A calculated field called:

```text
total_amount
```

was added.

It is calculated as:

```text
quantity × unit_price
```

This gives us a basic business metric that can later be used for analytics.

---

## Processed Dataset

After ingestion and cleaning, the data is saved to:

```text
data/processed/orders_clean.csv
```

At this point the pipeline became:

```text
Raw CSV
   ↓
Python
   ↓
Validation
   ↓
Cleaning
   ↓
Transformation
   ↓
Processed CSV
```

---

# Day 3 — MySQL Raw Warehouse Layer

Day 3 was the first time the project moved from local files into an actual database.

I already had **MySQL installed locally**, so I decided to use MySQL instead of PostgreSQL for this project.

The current architecture is:

```text
orders.csv
    ↓
Python Ingestion
    ↓
orders_clean.csv
    ↓
Python MySQL Loader
    ↓
MySQL
    ↓
raw_orders
```

---

## MySQL Database

I created a MySQL database:

```text
ecommerce_warehouse
```

Inside it, the first warehouse table is:

```text
raw_orders
```

This table represents the raw warehouse layer of the pipeline.

---

## Database Connection

Database credentials are stored in a local `.env` file rather than directly inside the Python code.

Example:

```text
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ecommerce_warehouse
DB_USER=root
DB_PASSWORD=********
```

The `.env` file is included in `.gitignore` so database credentials are not uploaded to GitHub.

---

## MySQL Connection

The database connection is handled by:

```text
ingestion/database.py
```

The project uses:

```text
mysql-connector-python
```

to connect Python with MySQL.

The connection can be tested using:

```bash
python -m ingestion.database
```

A successful connection returns:

```text
MySQL connection successful.
```

---

# Loading Data Into MySQL

The processed CSV is loaded into MySQL using:

```text
ingestion/load_to_mysql.py
```

The script creates the `raw_orders` table if it doesn't already exist.

The table contains fields such as:

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
total_amount
```

---

## Duplicate Handling

One important improvement on Day 3 was handling duplicate orders.

The `order_id` is used as the primary key.

The loader uses:

```sql
ON DUPLICATE KEY UPDATE
```

This means running the ingestion script multiple times doesn't simply insert the same order again.

For example:

```text
First run  → 10 records
Second run → still 10 records
```

instead of:

```text
First run  → 10 records
Second run → 20 records
```

This is an early step toward making the pipeline safe to run repeatedly.

---

# Data Verification

After loading the data, I verified it directly in MySQL.

For example:

```sql
SELECT *
FROM raw_orders;
```

To check the number of records:

```sql
SELECT COUNT(*) AS total_rows
FROM raw_orders;
```

And to calculate total revenue:

```sql
SELECT
    SUM(total_amount) AS total_revenue
FROM raw_orders;
```

I also tested basic aggregation:

```sql
SELECT
    category,
    SUM(total_amount) AS revenue
FROM raw_orders
GROUP BY category
ORDER BY revenue DESC;
```

This confirmed that the data successfully moved from Python into MySQL without losing the expected information.

---

# Current Architecture

After Day 3, the pipeline looks like:

```text
                    RAW DATA
                       │
                       ▼
                orders.csv
                       │
                       ▼
              Python Ingestion
                       │
              ┌────────┴────────┐
              │                 │
         Validation          Cleaning
              │                 │
              └────────┬────────┘
                       ▼
              orders_clean.csv
                       │
                       ▼
             Python MySQL Loader
                       │
                       ▼
                ┌─────────────┐
                │    MySQL    │
                │             │
                │ ecommerce_  │
                │ warehouse   │
                └──────┬──────┘
                       │
                       ▼
                  raw_orders
```

---

# Current Project Structure

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
│   ├── load_orders.py
│   ├── database.py
│   └── load_to_mysql.py
│
├── sql/
├── dbt_project/
├── airflow/
├── dashboard/
├── tests/
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

---

# What I've Learned So Far

After the first three days, the project has covered the basic foundation of a data warehouse pipeline.

I've worked with:

- Python data ingestion
- Pandas
- CSV processing
- Data validation
- Data cleaning
- Data type conversion
- Basic business transformations
- MySQL
- Python-to-MySQL connectivity
- Database credentials using environment variables
- Raw warehouse tables
- Primary keys
- Duplicate handling
- Basic SQL analytics

More importantly, the project is starting to resemble an actual data pipeline rather than just a data analysis script.

---

# What's Next?

## Day 4 — Incremental Data Loading

The next step is to make the pipeline more realistic.

Instead of loading the complete dataset every time, I'll introduce an **incremental loading approach**.

The planned flow will become:

```text
New / Updated Data
       ↓
Python Ingestion
       ↓
Detect Existing Orders
       ↓
Insert New Records
       ↓
Update Existing Records
       ↓
MySQL
```

This will help introduce concepts such as:

- Incremental processing
- Upserts
- Data freshness
- Load timestamps
- Change detection
- Repeatable pipelines

---

# Project Status

**Day 3/12 completed — Development in Progress**

Current milestone:

```text
Raw CSV
   ↓
Python Ingestion
   ↓
Validation & Cleaning
   ↓
Processed CSV
   ↓
MySQL
   ↓
raw_orders
```

✅ Python ingestion completed  
✅ Data validation completed  
✅ Data cleaning completed  
✅ MySQL database created  
✅ Python → MySQL connection completed  
✅ Raw warehouse table created  
✅ Duplicate handling added  
✅ Data verified using SQL  

Next milestone:

**Build incremental data loading.**

---
## Day 3 Update

Completed the MySQL raw warehouse layer and connected the Python ingestion pipeline to MySQL.
## Author

**Kartik Dhyani**

Aspiring Data Engineer interested in Python, SQL, Data Warehousing, ETL/ELT pipelines, analytics engineering, batch processing, and modern Data Engineering tools.
