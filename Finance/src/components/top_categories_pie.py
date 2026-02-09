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

TOP_N = 5  # Top 5 categories

def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.TOP_CATEGORIES_PIE, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_top_categories(years, months, categories):
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
            return html.Div("No data selected.", id=ids.TOP_CATEGORIES_PIE)

        summary = (
            filtered.groupby(DataSchema.CATEGORY)[DataSchema.AMOUNT]
            .sum()
            .sort_values(ascending=False)
        )

        if len(summary) > TOP_N:
            top = summary.head(TOP_N)
            other = pd.Series([summary[TOP_N:].sum()], index=["Other"])
            summary = pd.concat([top, other])

        pie = go.Pie(
            labels=summary.index,
            values=summary.values,
            hole=0.5,
            marker=dict(colors=COLOR_SEQUENCE),
            hovertemplate="<b>%{label}</b><br>$%{value:,.2f}<br>%{percent}<extra></extra>",
        )

        fig = go.Figure(data=[pie])
        fig.update_layout(**DARK_LAYOUT, title=f"Top {TOP_N} Categories", margin=dict(t=50, b=20, l=20, r=20))

        return html.Div(dcc.Graph(figure=fig), id=ids.TOP_CATEGORIES_PIE)

    return html.Div(id=ids.TOP_CATEGORIES_PIE)
