import base64
import io
import pandas as pd
import dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
from src.data.loader import load_transaction_data
from src.components import ids
from src.components.summary_cards import render as summary_render
from src.components.bar_chart import render as bar_chart_render
from src.components.line_chart import render as line_chart_render
from src.components.stacked_bar_chart import render as stacked_bar_chart_render
from src.components.pie_chart import render as pie_chart_render
from src.components.top_categories_pie import render as top_categories_pie_render
from src.components.year_dropdown import render as year_dropdown_render
from src.components.month_dropdown import render as month_dropdown_render
from src.components.category_dropdown import render as category_dropdown_render

# Load default data (optional)
default_data = load_transaction_data("data/transactions.csv")

app = Dash(__name__)
app.title = "Finance Dashboard"

# Layout with upload + all components
app.layout = html.Div(
    className="dashboard-container",
    children=[
        html.H2("Personal Finance Dashboard"),

        # -------- CSV Upload --------
        dcc.Upload(
            id=ids.UPLOAD_COMPONENT,
            children=html.Div("Drag & Drop or Click to Upload CSV"),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "10px",
                "textAlign": "center",
                "marginBottom": "20px",
                "cursor": "pointer",
            },
            multiple=False,
        ),

        html.Div(id=ids.UPLOAD_STATUS),
        dcc.Store(id=ids.DATA_STORE, data=default_data.to_dict("records")),

        # -------- Filter Dropdowns --------
        html.Div(
            className="dropdown-container",
            children=[
                year_dropdown_render(app, default_data),
                month_dropdown_render(app, default_data),
                category_dropdown_render(app, default_data),
            ],
        ),

        # -------- Dashboard Sections --------
        summary_render(app),
        html.Div(style={"height": "20px"}),  # spacing
        html.Div(
            className="charts-row",
            children=[
                html.Div(bar_chart_render(app), className="chart-container"),
                html.Div(pie_chart_render(app), className="chart-container"),
            ],
        ),
        html.Div(
            className="charts-row",
            children=[
                html.Div(line_chart_render(app), className="chart-container"),
                html.Div(stacked_bar_chart_render(app), className="chart-container"),
            ],
        ),
        html.Div(
            className="charts-row",
            children=[
                html.Div(top_categories_pie_render(app), className="chart-container"),
            ],
        ),
    ],
)

# -------- Upload Callback --------
@app.callback(
    Output(ids.DATA_STORE, "data"),
    Output(ids.UPLOAD_STATUS, "children"),
    Input(ids.UPLOAD_COMPONENT, "contents"),
    State(ids.UPLOAD_COMPONENT, "filename"),
    prevent_initial_call=True,
)
def update_data(contents, filename):
    if not contents:
        return dash.no_update, ""
    
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    try:
        if not filename.endswith(".csv"):
            return dash.no_update, "Please upload a CSV file."

        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        df.columns = df.columns.str.strip()

        required = ["date", "category", "amount"]
        if not all(col in df.columns for col in required):
            return dash.no_update, "CSV must contain: date, category, amount."

        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])

        df["year"] = df["date"].dt.year.astype(str)
        df["month"] = df["date"].dt.month.astype(str)

        return df.to_dict("records"), f"Uploaded {filename} successfully."

    except Exception as e:
        return dash.no_update, f"Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
