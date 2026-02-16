import pandas as pd
from dash import Dash, html
from dash.dependencies import Input, Output
from ..data.loader import DataSchema
from . import ids

def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.SUMMARY_CARDS, "children"),
        [
            Input(ids.DATA_STORE, "data"),
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_summary(stored_data, years, months, categories):
        if not stored_data:
            return [html.Div("No data selected.", className="summary-card")]

        df = pd.DataFrame(stored_data)
        df[DataSchema.MONTH] = df[DataSchema.MONTH].astype(int)
        start_month, end_month = months

        filtered = df[
            (df[DataSchema.YEAR].isin(years)) &
            (df[DataSchema.MONTH].between(start_month, end_month)) &
            (df[DataSchema.CATEGORY].isin(categories))
        ]

        if filtered.empty:
            return [html.Div("No data selected.", className="summary-card")]

        total_spent = filtered[DataSchema.AMOUNT].sum()
        avg_monthly = filtered.groupby(DataSchema.MONTH)[DataSchema.AMOUNT].sum().mean()
        top_category = filtered.groupby(DataSchema.CATEGORY)[DataSchema.AMOUNT].sum().idxmax()

        return [
            html.Div(className="summary-card", children=[
                html.H6("Total Spent"),
                html.P(f"${total_spent:,.2f}", className="summary-value")
            ]),
            html.Div(className="summary-card", children=[
                html.H6("Top Category"),
                html.P(top_category, className="summary-value")
            ]),
            html.Div(className="summary-card", children=[
                html.H6("Average Monthly"),
                html.P(f"${avg_monthly:,.2f}", className="summary-value")
            ]),
        ]

    return html.Div(id=ids.SUMMARY_CARDS, className="summary-cards")
