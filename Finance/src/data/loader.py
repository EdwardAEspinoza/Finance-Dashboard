import pandas as pd

class DataSchema:
    AMOUNT = "amount"
    CATEGORY = "category"
    DATE = "date"
    MONTH = "month"
    YEAR = "year"


def load_transaction_data(path: str) -> pd.DataFrame:
    """
    Loads transaction data from a CSV file and processes it for the dashboard.

    Steps:
    1. Reads CSV
    2. Strips any extra spaces from column names
    3. Converts 'date' column to datetime
    4. Drops rows with invalid dates
    5. Creates 'year' and 'month' columns as strings
    """
    # Load CSV
    data = pd.read_csv(path)

    # Strip spaces from column names (common CSV issue)
    data.columns = data.columns.str.strip()

    # Ensure 'date' is datetime
    data[DataSchema.DATE] = pd.to_datetime(data[DataSchema.DATE], errors="coerce")

    # Drop rows with invalid dates
    data = data.dropna(subset=[DataSchema.DATE]).reset_index(drop=True)

    # Create year and month columns as strings
    data[DataSchema.YEAR] = data[DataSchema.DATE].dt.year.astype(str)
    data[DataSchema.MONTH] = data[DataSchema.DATE].dt.month.astype(str)

    return data
