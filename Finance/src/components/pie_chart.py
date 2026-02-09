import pandas as pd
import plotly.graph_objects as go
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
        Output(ids.PIE_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_pie_chart(
        years: list[str], months: list[str], categories: list[str]
    ) -> html.Div:

        filtered_data = data.query(
            "year in @years and month in @months and category in @categories"
        )

        if filtered_data.empty:
            return html.Div("No data selected.", id=ids.PIE_CHART)

        summary = (
            filtered_data
            .groupby(DataSchema.CATEGORY)[DataSchema.AMOUNT]
            .sum()
            .reset_index()
        )

        pie = go.Pie(
            labels=summary[DataSchema.CATEGORY],
            values=summary[DataSchema.AMOUNT],
            hole=0.5,
            marker=dict(colors=COLOR_SEQUENCE),
            hovertemplate="<b>%{label}</b><br>$%{value:,.2f}<br>%{percent}<extra></extra>",
        )

        fig = go.Figure(data=[pie])
        fig.update_layout(
            **DARK_LAYOUT,
            title="Spending Distribution",
            margin=dict(t=50, b=20, l=20, r=20),
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.PIE_CHART)

    return html.Div(id=ids.PIE_CHART)
