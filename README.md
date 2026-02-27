# FinanceScope Insight – Personal Finance Dashboard

An interactive financial analytics dashboard built with **Python**, **Dash**, and **Plotly**. It allows users to upload CSV transaction data and explore income and expense trends across customizable time ranges with dynamic, real-time visualizations.

## Features

- **Time-Series Analysis**: Visualize trends over days, months, and years.
- **Dynamic Charts**: Bar, line, pie, and stacked charts update in real time based on user input.
- **Category-Based Grouping**: Transactions are grouped by category for detailed insights.
- **Responsive Filtering**: Choose date ranges and categories via dropdowns; charts update through Dash callbacks.
- **Data Processing**: Pandas handles cleaning, transformation, aggregation, and efficient analysis of user-uploaded CSV datasets.
- **Customizable Layout**: Modular components (charts, dropdowns, summary cards) defined in `src/components`.

## Technologies

- Python 3.x
- [Dash](https://dash.plotly.com/) for the web interface
- [Plotly](https://plotly.com/python/) for interactive visualizations
- [Pandas](https://pandas.pydata.org/) for data manipulation

## Getting Started

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd "Finance Dashboard/Finance"
   ```
2. Create and activate a virtual environment (conda or venv).
3. Install dependencies:
   ```bash
   pip install -r environment/requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```
5. Open your browser at `http://127.0.0.1:8050` and upload a transactions CSV file to begin.


```

