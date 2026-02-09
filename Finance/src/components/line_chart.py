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

COLOR_SEQUENCE = ["#38bdf8"]

def render(app: Dash, data: pd.DataFrame) -> html.Div:

    @app.callback(
        Output(ids.LINE_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_line_chart(years, months, categories):

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
            return html.Div("No data selected.", id=ids.LINE_CHART)

        # Sum by month-year
        filtered["month_year"] = filtered[DataSchema.DATE].dt.to_period("M")
        monthly_sum = (
            filtered.groupby("month_year")[DataSchema.AMOUNT]
            .sum()
            .reset_index()
        )
        monthly_sum["month_year"] = monthly_sum["month_year"].dt.to_timestamp()

        fig = px.line(
            monthly_sum,
            x="month_year",
            y=DataSchema.AMOUNT,
            markers=True,
            title="Monthly Spending Trend",
            color_discrete_sequence=COLOR_SEQUENCE,
        )

        fig.update_layout(
            **DARK_LAYOUT,
            xaxis_title="Month",
            yaxis_title="Total Amount ($)",
            margin=dict(t=50, b=40, l=40, r=20),
        )

        fig.update_traces(
            hovertemplate="$%{y:,.2f}<br>%{x|%b %Y}<extra></extra>"
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.LINE_CHART)

    return html.Div(id=ids.LINE_CHART)
