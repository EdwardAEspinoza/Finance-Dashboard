from dash import Dash, html
from src.components import (
    bar_chart,
    pie_chart,
    line_chart,
    stacked_bar_chart,
    top_categories_pie,
    summary_cards,
    year_dropdown,
    month_dropdown,
    category_dropdown,
)


def create_layout(app: Dash, data):
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title, style={"textAlign": "center", "marginBottom": "20px"}),
            html.Hr(),

            # Summary cards
            summary_cards.render(app, data),

            # Filters
            html.Div(
                className="dropdown-container",
                children=[
                    year_dropdown.render(app, data),
                    month_dropdown.render(app, data),
                    category_dropdown.render(app, data),
                ],
            ),

            # First row: Bar chart + Pie chart
            html.Div(
                className="charts-row",
                children=[
                    html.Div(bar_chart.render(app, data), className="chart-container"),
                    html.Div(pie_chart.render(app, data), className="chart-container"),
                ],
            ),

            # Second row: Line chart + Stacked bar chart
            html.Div(
                className="charts-row",
                children=[
                    html.Div(line_chart.render(app, data), className="chart-container"),
                    html.Div(stacked_bar_chart.render(app, data), className="chart-container"),
                ],
            ),

            # Optional row: Top N categories pie chart
            html.Div(
                className="charts-row",
                children=[
                    html.Div(top_categories_pie.render(app, data), className="chart-container"),
                ],
            ),
        ],
    )
