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
    # Ensure month is integer
    data[DataSchema.MONTH] = data[DataSchema.MONTH].astype(int)

    @app.callback(
        Output(ids.BAR_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_bar_chart(years, months, categories):
        start_month, end_month = months

        # Boolean mask filtering
        mask = (
            data[DataSchema.YEAR].isin(years)
            & data[DataSchema.MONTH].between(start_month, end_month)
            & data[DataSchema.CATEGORY].isin(categories)
        )
        filtered_data = data[mask]

        if filtered_data.empty:
            return html.Div("No data selected.", id=ids.BAR_CHART)

        pivot = (
            filtered_data
            .groupby(DataSchema.CATEGORY)[DataSchema.AMOUNT]
            .sum()
            .reset_index()
            .sort_values(DataSchema.AMOUNT, ascending=False)
        )

        fig = px.bar(
            pivot,
            x=DataSchema.CATEGORY,
            y=DataSchema.AMOUNT,
            color=DataSchema.CATEGORY,
            title="Spending by Category",
            color_discrete_sequence=COLOR_SEQUENCE,
        )

        fig.update_layout(
            **DARK_LAYOUT,
            xaxis_title="Category",
            yaxis_title="Total Amount ($)",
            showlegend=False,
            margin=dict(t=50, l=40, r=20, b=40),
        )

        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>$%{y:,.2f}<extra></extra>"
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)
