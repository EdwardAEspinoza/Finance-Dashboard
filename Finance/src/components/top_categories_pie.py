import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from ..data.loader import DataSchema
from . import ids

COLOR_SEQUENCE = ["#38bdf8", "#22c55e", "#f97316", "#e11d48", "#a855f7"]
TOP_N = 5
DARK_LAYOUT = dict(
    paper_bgcolor="#1e293b",
    plot_bgcolor="#1e293b",
    font=dict(color="#e5e7eb"),
    title_font=dict(size=16, color="#e5e7eb"),
)

def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.TOP_CATEGORIES_PIE, "children"),
        [
            Input(ids.DATA_STORE, "data"),
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_chart(stored_data, years, months, categories):
        if not stored_data:
            return html.Div("No data selected.", id=ids.TOP_CATEGORIES_PIE)

        df = pd.DataFrame(stored_data)
        df[DataSchema.MONTH] = df[DataSchema.MONTH].astype(int)
        start_month, end_month = months

        filtered = df[
            (df[DataSchema.YEAR].isin(years)) &
            (df[DataSchema.MONTH].between(start_month, end_month)) &
            (df[DataSchema.CATEGORY].isin(categories))
        ]

        if filtered.empty:
            return html.Div("No data selected.", id=ids.TOP_CATEGORIES_PIE)

        summary = filtered.groupby(DataSchema.CATEGORY)[DataSchema.AMOUNT].sum().sort_values(ascending=False)
        if len(summary) > TOP_N:
            top = summary.head(TOP_N)
            other = pd.Series([summary[TOP_N:].sum()], index=["Other"])
            summary = pd.concat([top, other])

        fig = go.Figure(go.Pie(
            labels=summary.index,
            values=summary.values,
            hole=0.5,
            marker=dict(colors=COLOR_SEQUENCE),
            hovertemplate="<b>%{label}</b><br>$%{value:,.2f}<br>%{percent}<extra></extra>",
        ))
        fig.update_layout(DARK_LAYOUT, title=f"Top {TOP_N} Categories", margin=dict(t=50, b=20, l=20, r=20))

        return html.Div(dcc.Graph(figure=fig), id=ids.TOP_CATEGORIES_PIE)

    return html.Div(id=ids.TOP_CATEGORIES_PIE)
