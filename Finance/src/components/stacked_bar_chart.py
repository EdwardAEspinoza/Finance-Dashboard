import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from ..data.loader import DataSchema
from . import ids

COLOR_SEQUENCE = ["#38bdf8", "#22c55e", "#f97316", "#e11d48", "#a855f7"]
DARK_LAYOUT = dict(
    paper_bgcolor="#1e293b",
    plot_bgcolor="#1e293b",
    font=dict(color="#e5e7eb"),
    title_font=dict(size=16, color="#e5e7eb"),
)

def render(app: Dash) -> html.Div:
    @app.callback(
        Output(ids.STACKED_BAR_CHART, "children"),
        [
            Input(ids.DATA_STORE, "data"),
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_chart(stored_data, years, months, categories):
        if not stored_data:
            return html.Div("No data selected.", id=ids.STACKED_BAR_CHART)

        df = pd.DataFrame(stored_data)
        df[DataSchema.DATE] = pd.to_datetime(df[DataSchema.DATE])
        df[DataSchema.MONTH] = df[DataSchema.MONTH].astype(int)
        start_month, end_month = months

        filtered = df[
            (df[DataSchema.YEAR].isin(years)) &
            (df[DataSchema.MONTH].between(start_month, end_month)) &
            (df[DataSchema.CATEGORY].isin(categories))
        ]

        if filtered.empty:
            return html.Div("No data selected.", id=ids.STACKED_BAR_CHART)

        filtered["month_year"] = filtered[DataSchema.DATE].dt.to_period("M")
        pivot = filtered.groupby(["month_year", DataSchema.CATEGORY])[DataSchema.AMOUNT].sum().reset_index()
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
            margin=dict(t=50, l=40, r=20, b=40),
        )
        fig.update_traces(hovertemplate="<b>%{label}</b><br>$%{y:,.2f}<br>%{x|%b %Y}<extra></extra>")

        return html.Div(dcc.Graph(figure=fig), id=ids.STACKED_BAR_CHART)

    return html.Div(id=ids.STACKED_BAR_CHART)
