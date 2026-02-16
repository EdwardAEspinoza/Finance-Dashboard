import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_years: list[str] = data[DataSchema.YEAR].tolist()
    unique_years = sorted(set(all_years), key=int)

    @app.callback(
        Output(ids.YEAR_DROPDOWN, "options"),
        Output(ids.YEAR_DROPDOWN, "value"),
        Input(ids.DATA_STORE, "data")
    )
    def update_year_options(stored_data):
        if not stored_data:
            return [], []
        df = pd.DataFrame(stored_data)
        years = sorted(set(df[DataSchema.YEAR].astype(str)), key=lambda x: int(x))
        options = [{"label": year, "value": year} for year in years]
        return options, years

    return html.Div(
        children=[
            html.H6("Year"),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=[{"label": year, "value": year} for year in unique_years],
                value=unique_years,
                multi=True,
            ),
        ]
    )