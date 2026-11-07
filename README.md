# Synergizing Success: Improving Operational Efficiency and Employee Engagement

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Charts-Plotly-3F4F75)](https://plotly.com/python/)

## Project Overview

An interactive Streamlit dashboard for exploring restaurant-level
operational data, including restaurant categories, customer ratings,
rating counts, average listed cost, online ordering, table booking,
cuisine types, locations and delivery time.

The application includes reproducible built-in demo data, CSV upload,
sidebar filters, interactive Plotly charts, a searchable data table
and CSV export.

**Important source-data clarification:** The supplied Jomato.csv
contains restaurant fields. It does not contain employee names,
departments, employee performance scores, sales revenue or profit
margins. This implementation does not fabricate those KPIs.

## Key SQL Features Used

The supplied SQL script demonstrates:

- **User-defined scalar function:** `dbo.fn_StuffChicken`
  uses `STUFF()` to insert text into the restaurant type.
- **Conditional logic:** `CASE` assigns rating status labels
  such as Excellent, Good, Average and Bad.
- **Numeric functions:** `CEILING()`, `FLOOR()` and `ABS()`.
- **Date functions:** `GETDATE()`, `YEAR()`, `DATENAME()` and `DAY()`.
- **Aggregation with ROLLUP:** Summarizes `AverageCost` by
  restaurant type and includes a grand-total row.
- **Top-N query:** `TOP 1 ... ORDER BY` identifies the restaurant
  with the highest number of ratings.

**Not present in the supplied SQL script:** Window functions,
triggers or views. They are not claimed as implemented features.

## Dashboard Features

- Built-in deterministic demo data.
- CSV upload and column validation.
- Sidebar filters for area, restaurant type, online ordering,
  rating and average cost.
- KPI cards for record count, average rating, average listed
  cost and average delivery time.
- Plotly charts for restaurant mix, area ratings, listed cost,
  rating vs. cost, online ordering and delivery time.
- Searchable data table and filtered CSV download.

## Tech Stack

- Python 3.10+
- Streamlit
- Pandas
- Plotly

## Local Installation Guide

1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Create a virtual environment:

   ```bash
   python -m venv .venv
