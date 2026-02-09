import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from ..data.loader import DataSchema
from . import ids

def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_months = data[DataSchema.MONTH].astype(int).tolist()
    unique_months = sorted(set(all_months))

    MONTH_NAMES = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    marks = {m: MONTH_NAMES[m-1] for m in unique_months}

    @app.callback(
        Output(ids.MONTH_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_MONTHS_BUTTON, "n_clicks"),
    )
    def select_all_months(_: int) -> list[int]:
        return [min(unique_months), max(unique_months)]  # ✅ return only two numbers

    return html.Div(
        children=[
            html.H6("Month"),
            dcc.RangeSlider(
                id=ids.MONTH_DROPDOWN,
                min=min(unique_months),
                max=max(unique_months),
                step=1,
                value=[min(unique_months), max(unique_months)],  # ✅ must be two numbers
                marks=marks,
                tooltip={"placement": "bottom", "always_visible": True},
                allowCross=False,
            ),
            html.Button(
                className="dropdown-button",
                children=["Select All"],
                id=ids.SELECT_ALL_MONTHS_BUTTON,
                n_clicks=0,
            ),
        ]
    )
