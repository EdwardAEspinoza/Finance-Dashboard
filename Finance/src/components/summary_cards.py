import pandas as pd
from dash import Dash, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.SUMMARY_CARDS, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_summary_cards(years, months, categories):
        filtered = data.query(
            "year in @years and month in @months and category in @categories"
        )

        if filtered.empty:
            return html.Div("No data selected.")

        total_spent = filtered[DataSchema.AMOUNT].sum()
        avg_monthly = (
            filtered.groupby(DataSchema.MONTH)[DataSchema.AMOUNT].sum().mean()
        )
        top_category = (
            filtered.groupby(DataSchema.CATEGORY)[DataSchema.AMOUNT]
            .sum()
            .idxmax()
        )

        return [
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
                    html.P(top_category, className="summary-value"),
                ],
            ),
            html.Div(
                className="summary-card",
                children=[
                    html.H6("Average Monthly"),
                    html.P(f"${avg_monthly:,.2f}", className="summary-value"),
                ],
            ),
        ]

    return html.Div(id=ids.SUMMARY_CARDS, className="summary-cards")
