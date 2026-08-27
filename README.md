# Day 4 — Incremental Data Loading

Today I improved the pipeline so it can handle data in a more realistic way instead of simply loading the same records again and again.

The main focus was **incremental loading and upserts in MySQL**.

---

## What I Worked On

Previously, the pipeline looked like:

```text
CSV
 ↓
Python
 ↓
Clean Data
 ↓
MySQL
