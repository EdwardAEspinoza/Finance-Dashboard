import pandas as pd
from dash import Dash, html
from src.components import (
    bar_chart,
    category_dropdown,
    month_dropdown,
    pie_chart,
    year_dropdown,
)


def create_layout(app: Dash, data: pd.DataFrame) -> html.Div:
    # Calculate summary stats
    total_spent = data['amount'].sum()
    top_category = data.groupby('category')['amount'].sum().idxmax()
    average_monthly = data.groupby('month')['amount'].sum().mean()

    # Layout
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title, style={"textAlign": "center", "marginBottom": "20px"}),
            html.Hr(),

            # Summary cards
            html.Div(
                className="summary-cards",
                children=[
                    html.Div(
                        className="summary-card",
                        children=[
                            html.H6("Total Spent"),
                            html.P(f"${total_spent:,.2f}", className="summary-value"),
                        ],
                    ),
                    html.Div(
                        className="summary-card",
                        children=[
                            html.H6("Top Category"),
                            html.P(f"{top_category}", className="summary-value"),
                        ],
                    ),
                    html.Div(
                        className="summary-card",
                        children=[
                            html.H6("Average Monthly"),
                            html.P(f"${average_monthly:,.2f}", className="summary-value"),
                        ],
                    ),
                ],
            ),

            # Filters
            html.Div(
                className="dropdown-container",
                children=[
                    year_dropdown.render(app, data),
                    month_dropdown.render(app, data),
                    category_dropdown.render(app, data),
                ],
            ),

            # Charts
            html.Div(
                className="charts-row",
                children=[
                    html.Div(bar_chart.render(app, data), className="chart-container"),
                    html.Div(pie_chart.render(app, data), className="chart-container"),
                ],
            ),
        ],
    )
