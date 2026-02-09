import pandas as pd
from dash import Dash, html

from src.components import (
    bar_chart,
    category_dropdown,
    month_dropdown,
    pie_chart,
    year_dropdown,
    summary_cards,
)


def create_layout(app: Dash, data: pd.DataFrame) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title, style={"textAlign": "center", "marginBottom": "20px"}),
            html.Hr(),

            # ✅ Reactive summary cards
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
