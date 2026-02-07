import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from . import ids


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

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.PIE_CHART)

        pie = go.Pie(
            labels=filtered_data[DataSchema.CATEGORY],
            values=filtered_data[DataSchema.AMOUNT],
            hole=0.5,
            hovertemplate="<b>%{label}</b><br>$%{value:,.2f}<br>%{percent}<extra></extra>",
        )

        fig = go.Figure(data=[pie])
        fig.update_layout(
            title="Spending Distribution",
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(t=50, b=20, l=20, r=20),
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.PIE_CHART)

    return html.Div(id=ids.PIE_CHART)