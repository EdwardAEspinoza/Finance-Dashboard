from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from src.components import (
    summary_cards,
    pie_chart,
    bar_chart,
    line_chart,
    stacked_bar_chart,
    top_categories_pie,
)
from src.components.layout import create_layout
from src.data.loader import load_transaction_data

DATA_PATH = "./data/transactions.csv"


def main() -> None:
    # Load data
    data = load_transaction_data(DATA_PATH)

    # Create Dash app
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Financial Dashboard"

    # Set layout with all components
    app.layout = create_layout(app, data)

    # Run the app
    app.run()


if __name__ == "__main__":
    main()
