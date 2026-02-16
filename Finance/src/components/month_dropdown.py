import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from ..data.loader import DataSchema
from . import ids

def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_months = data[DataSchema.MONTH].astype(int).tolist()
    unique_months = sorted(set(all_months))

    MONTH_NAMES = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    @app.callback(
        Output(ids.MONTH_DROPDOWN, "min"),
        Output(ids.MONTH_DROPDOWN, "max"),
        Output(ids.MONTH_DROPDOWN, "marks"),
        Output(ids.MONTH_DROPDOWN, "value"),
        Input(ids.DATA_STORE, "data")
    )
    def update_month_options(stored_data):
        if not stored_data:
            return 1, 12, {}, [1, 12]
        df = pd.DataFrame(stored_data)
        months = sorted(set(df[DataSchema.MONTH].astype(int)))
        marks = {m: MONTH_NAMES[m-1] for m in months}
        return min(months), max(months), marks, [min(months), max(months)]

    marks = {m: MONTH_NAMES[m-1] for m in unique_months}

    return html.Div(
        children=[
            html.H6("Month"),
            dcc.RangeSlider(
                id=ids.MONTH_DROPDOWN,
                min=min(unique_months),
                max=max(unique_months),
                step=1,
                value=[min(unique_months), max(unique_months)],
                marks=marks,
                tooltip={"placement": "bottom", "always_visible": True},
                allowCross=False,
            ),
        ]
    )
