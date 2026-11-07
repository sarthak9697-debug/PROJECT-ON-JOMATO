# 📊 Synergizing Success: Improving Operational Efficiency and Employee Engagement

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A recruiter-friendly, production-ready Streamlit web application designed to bridge robust SQL data engineering principles with executive business intelligence. This platform analyzes operational efficiency, employee performance scores, revenue streams, and profit margins across business departments.

---

## 🚀 Project Overview

The **"Synergizing Success"** dashboard empowers executives and operations managers to explore multi-dimensional operational metrics. It features an embedded fallback dataset simulating enterprise-grade databases, allowing instant exploration on Streamlit Community Cloud without requiring a live SQL server connection.

### ✨ Key Features
- **Interactive Control Panels**: Real-time filtering by department, employee performance score, profit margin range, and keyword search.
- **Executive KPI Summary Cards**: Instant visibility into Total Revenue, Average Profit Margins, Employee Performance, Net Profit, and Active Headcount.
- **Advanced Plotly Visualizations**:
  - Departmental Revenue vs. Net Profit Comparison
  - Employee Performance vs. Revenue Scatter Analysis (sized by net profit)
  - Departmental Operational Efficiency Index Box Plots
  - Operational Cost Distribution by Category
- **Interactive Data Grid & Export**: Filterable dataframe viewer with one-click CSV export functionality.

---

## 🛠️ Key SQL Features & Architecture

Underpinning this application's data architecture are advanced SQL query structures and database design concepts:

1. **Window Functions**: Utilized in backend data pipelines for running totals, department-level rankings (`RANK()`, `DENSE_RANK()`), and moving averages of employee performance versus cost.
2. **User-Defined Functions (UDFs) & Stored Procedures**: Custom calculation wrappers (e.g., dynamic efficiency score computations and string normalization for operational categories).
3. **Database Views**: Pre-aggregated views (`vw_DepartmentPerformanceSummary`) joining employee metrics with financial ledgers to optimize analytical query performance.
4. **ROLLUP & GROUPING SETS**: Multi-level aggregations to calculate sub-totals and grand totals for operational costs across departmental hierarchies.
5. **Triggers**: Automated audit and logging triggers on transaction tables to monitor real-time updates to profit margins and employee status changes.

---

## 🧰 Tech Stack

- **Frontend & UI**: Streamlit
- **Data Manipulation & Analysis**: Pandas, NumPy
- **Data Visualization**: Plotly
- **Deployment**: Streamlit Community Cloud

---

## 📦 Local Installation Guide

Follow these steps to run the application locally on your machine:

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/your-username/synergizing-success-dashboard.git](https://github.com/your-username/synergizing-success-dashboard.git)
   cd synergizing-success-dashboard