# FinanceScope Insight – Personal Finance Dashboard

FinanceScope Insight is an interactive personal finance dashboard built with Python, Dash, and Plotly. It helps users visualize income, expenses, and savings trends across customizable time ranges, explore transaction-level data, and surface actionable insights through responsive, shareable charts and filters.

## Overview

FinanceScope Insight lets you upload or load CSV transaction data and quickly analyze spending and income patterns using interactive charts, real-time filters, and time-series aggregation. It focuses on clarity, performance, and extensibility so you can customize categories, detect trends, and export results for reporting.

## Key Features

- **Interactive visualizations**: bar, line, pie, and stacked charts powered by Plotly.
- **Dynamic filtering**: real-time date range, month, year, and category filters using Dash callbacks.
- **Pandas-backed data processing**: cleaning, transformation, category grouping, and aggregation for large CSVs.
- **Time-series analysis**: trend detection, rolling aggregates, and period-over-period comparisons.
- **Category analytics**: top categories, breakdowns, and stacked views for composition analysis.
- **Responsive UI**: adaptive layout for different screen sizes.
- **Export & share**: download filtered datasets or chart images where supported.
- **Extensible modular structure**: components under `src/components` for rapid feature additions.

## Additional Capabilities

- Robust parsing and normalization for dates, categories, and malformed rows.
- Custom category mapping and merging to standardize merchant/category labels.
- Caching of expensive aggregations to keep interactions snappy on large datasets.
- Accessible color palettes and detailed hover tooltips for exploration.
- Well-structured Dash callback orchestration to keep charts and controls synchronized.
- Unit-testable data loaders and transformers in `src/data/loader.py`.

## Tech Stack

- Python
- Dash
- Plotly
- Pandas
- Flask for advanced deployment

## Data Format

Expect a CSV with at least these columns:

- `date` — transaction date (ISO or common formats)
- `amount` — positive for income, negative for expenses (or use separate `income`/`expense` fields)
- `category` — transaction category
- `description` — optional

See `src/data/loader.py` for parsing/coercion rules.

## Installation

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
& .venv\Scripts\Activate.ps1
pip install -r environment/requirements.txt
```

Or with conda:

```powershell
conda env create -f environment/conda.yaml
conda activate finance-scope
```

## Run Locally

```powershell
python main.py
```

Open the Dash app (usually at `http://127.0.0.1:8050`).

## Usage

- Upload your CSV or replace `data/transactions.csv`.
- Use date/month/year/category controls to filter.
- Hover for exact values and click legends to toggle series.
