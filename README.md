# Cloud-Style ELT Data Warehouse Pipeline

I'm building this project to get hands-on experience with how a modern **ELT and Data Warehouse pipeline** works from end to end.

The idea is to start with raw business data, ingest it using Python, load it into PostgreSQL, transform it using SQL and dbt, and eventually automate the complete workflow using Apache Airflow.

Rather than building everything at once, I'm developing the project step by step so I can understand what each component is doing and why it is needed.

---

## Project Goal

The goal is to build a complete pipeline that eventually looks like:

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
Staging Layer
      ↓
Data Warehouse
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

The project will focus on both **Data Engineering** and **Analytics Engineering** concepts.

---

## Planned Tech Stack

The project will gradually use:

- Python
- Pandas
- SQL
- PostgreSQL
- dbt Core
- Apache Airflow
- Streamlit
- Pytest
- Git
- GitHub

Everything is being designed so the project can be developed locally using free and open-source tools.

---

## What I Want to Learn

Through this project, I want to get practical experience with:

- ETL vs ELT
- Data ingestion
- PostgreSQL
- Data warehouse design
- Raw and staging layers
- SQL transformations
- dbt models
- Fact tables
- Dimension tables
- Star schema
- Incremental loading
- Data quality testing
- Pipeline orchestration
- Apache Airflow
- Logging and monitoring
- Analytics-ready datasets
- Automated testing

---

## Development Roadmap

| Day | Implementation | Status |
|---|---|---|
| Day 1 | Project Setup & Architecture | ✅ |
| Day 2 | Data Source & Python Ingestion | ⏳ |
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

## Current Project Structure

```text
Cloud_ELT_Data_Warehouse/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── ingestion/
│
├── sql/
│
├── dbt_project/
│
├── airflow/
│
├── dashboard/
│
├── tests/
│
├── README.md
├── requirements.txt
└── .gitignore
```

The structure will grow as new components are added.

---

## Day 1

Day 1 is intentionally simple.

Today I:

- Planned the overall architecture
- Created the project structure
- Created the GitHub repository
- Added the initial dependencies
- Added `.gitignore`
- Created the first README
- Defined the development roadmap

The actual data pipeline starts from **Day 2**.

---

## Project Status

🚧 **Day 1/12 — Development in Progress**

Current milestone:

**Project Setup & Architecture ✅**

Next step: **Build the first Python data ingestion pipeline.**

---

## Author

**Kartik Dhyani**

Aspiring Data Engineer interested in building practical projects using Python, SQL, data warehousing, batch processing, real-time streaming, and modern Data Engineering tools.
