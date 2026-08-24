from pathlib import Path

import pandas as pd


RAW_FILE = Path("data/raw/orders.csv")
PROCESSED_DIR = Path("data/processed")
OUTPUT_FILE = PROCESSED_DIR / "orders_clean.csv"


def load_orders():
    """
    Load raw order data from CSV.
    """

    if not RAW_FILE.exists():
        raise FileNotFoundError(
            f"Raw dataset not found: {RAW_FILE}"
        )

    df = pd.read_csv(RAW_FILE)

    print("\nRaw data loaded successfully.")

    return df


def validate_orders(df):
    """
    Perform basic validation on order data.
    """

    required_columns = [
        "order_id",
        "customer_id",
        "customer_name",
        "product",
        "category",
        "quantity",
        "unit_price",
        "order_date",
        "city",
        "country",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    print("Required columns validated successfully.")


def clean_orders(df):
    """
    Apply basic cleaning and transformations.
    """

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    df = df.drop_duplicates()

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce",
    )

    df["unit_price"] = pd.to_numeric(
        df["unit_price"],
        errors="coerce",
    )

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce",
    )

    df = df.dropna(
        subset=[
            "order_id",
            "customer_id",
            "quantity",
            "unit_price",
            "order_date",
        ]
    )

    df = df[
        (df["quantity"] > 0)
        & (df["unit_price"] > 0)
    ]

    df["total_amount"] = (
        df["quantity"]
        * df["unit_price"]
    )

    return df


def save_clean_data(df):
    """
    Save cleaned order data.
    """

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print(
        f"Clean data saved to: {OUTPUT_FILE}"
    )


def run_ingestion():
    """
    Execute Day 2 ingestion pipeline.
    """

    print("=" * 60)
    print("Cloud ELT Data Warehouse - Order Ingestion")
    print("=" * 60)

    df = load_orders()

    print(
        f"\nRaw Rows    : {len(df)}"
    )

    validate_orders(df)

    clean_df = clean_orders(df)

    print(
        f"Clean Rows  : {len(clean_df)}"
    )

    print(
        f"Columns     : {len(clean_df.columns)}"
    )

    print(
        f"Total Sales : "
        f"{clean_df['total_amount'].sum():,.2f}"
    )

    save_clean_data(clean_df)

    print(
        "\nDay 2 ingestion completed successfully."
    )


if __name__ == "__main__":
    run_ingestion()