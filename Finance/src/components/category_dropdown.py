import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from ..data.loader import DataSchema
from . import ids

def render(app: Dash, data: pd.DataFrame = None) -> html.Div:
    # Get initial categories from the provided data
    initial_categories = []
    if data is not None and not data.empty:
        initial_categories = sorted(data[DataSchema.CATEGORY].unique().tolist())
    
    @app.callback(
        Output(ids.CATEGORY_DROPDOWN, "options"),
        Output(ids.CATEGORY_DROPDOWN, "value"),
        Input(ids.DATA_STORE, "data")
    )
    def update_categories(stored_data):
        if not stored_data:
            return [], []
        df = pd.DataFrame(stored_data)
        categories = sorted(df[DataSchema.CATEGORY].unique().tolist())
        options = [{"label": cat, "value": cat} for cat in categories]
        return options, categories

    return html.Div([
        html.H6("Category"),
        dcc.Dropdown(
            id=ids.CATEGORY_DROPDOWN, 
            multi=True, 
            placeholder="Select",
            value=initial_categories
        ),
    ])
