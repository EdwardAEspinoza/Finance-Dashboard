import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from . import ids

DARK_LAYOUT = dict(
    paper_bgcolor="#1e293b",
    plot_bgcolor="#1e293b",
    font=dict(color="#e5e7eb"),
    title_font=dict(size=16, color="#e5e7eb"),
)

COLOR_SEQUENCE = ["#38bdf8", "#22c55e", "#f97316", "#e11d48", "#a855f7"]

def render(app: Dash, data: pd.DataFrame) -> html.Div:

    @app.callback(
        Output(ids.STACKED_BAR_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_stacked_bar(years, months, categories):

        start_month, end_month = months
        # Convert month column to int first
        data[DataSchema.MONTH] = data[DataSchema.MONTH].astype(int)
        start_month = int(start_month)
        end_month = int(end_month)

        filtered = data[
            (data[DataSchema.YEAR].isin(years)) &
            (data[DataSchema.MONTH] >= start_month) &
            (data[DataSchema.MONTH] <= end_month) &
            (data[DataSchema.CATEGORY].isin(categories))
        ]

        if filtered.empty:
            return html.Div("No data selected.", id=ids.STACKED_BAR_CHART)

        filtered["month_year"] = filtered[DataSchema.DATE].dt.to_period("M")
        pivot = (
            filtered.groupby(["month_year", DataSchema.CATEGORY])[DataSchema.AMOUNT]
            .sum()
            .reset_index()
        )
        pivot["month_year"] = pivot["month_year"].dt.to_timestamp()

        fig = px.bar(
            pivot,
            x="month_year",
            y=DataSchema.AMOUNT,
            color=DataSchema.CATEGORY,
            title="Category Spending Over Time",
            color_discrete_sequence=COLOR_SEQUENCE,
        )

        fig.update_layout(
            **DARK_LAYOUT,
            xaxis_title="Month",
            yaxis_title="Amount ($)",
            margin=dict(t=50, b=40, l=40, r=20),
        )

        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>$%{y:,.2f}<br>%{x|%b %Y}<extra></extra>"
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.STACKED_BAR_CHART)

    return html.Div(id=ids.STACKED_BAR_CHART)
