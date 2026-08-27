from pathlib import Path

import pandas as pd

from ingestion.database import get_connection


INPUT_FILE = Path("data/processed/orders_clean.csv")


def create_table(connection):
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS raw_orders (
        order_id VARCHAR(50) PRIMARY KEY,
        customer_id VARCHAR(50),
        customer_name VARCHAR(150),
        product VARCHAR(150),
        category VARCHAR(100),
        quantity INT,
        unit_price DECIMAL(12, 2),
        order_date DATE,
        city VARCHAR(100),
        country VARCHAR(100),
        total_amount DECIMAL(14, 2),
        loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(query)
    connection.commit()
    cursor.close()

    print("raw_orders table is ready.")


def load_orders(connection, df):

    cursor = connection.cursor()

    insert_query = """
    INSERT INTO raw_orders (
        order_id,
        customer_id,
        customer_name,
        product,
        category,
        quantity,
        unit_price,
        order_date,
        city,
        country,
        total_amount
    )
    VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s
    )
    ON DUPLICATE KEY UPDATE
        customer_id = VALUES(customer_id),
        customer_name = VALUES(customer_name),
        product = VALUES(product),
        category = VALUES(category),
        quantity = VALUES(quantity),
        unit_price = VALUES(unit_price),
        order_date = VALUES(order_date),
        city = VALUES(city),
        country = VALUES(country),
        total_amount = VALUES(total_amount),
        loaded_at = CURRENT_TIMESTAMP
    """

    records = []

    for _, row in df.iterrows():

        records.append(
            (
                str(row["order_id"]),
                str(row["customer_id"]),
                str(row["customer_name"]),
                str(row["product"]),
                str(row["category"]),
                int(row["quantity"]),
                float(row["unit_price"]),
                row["order_date"].date(),
                str(row["city"]),
                str(row["country"]),
                float(row["total_amount"]),
            )
        )

    try:

        cursor.executemany(
            insert_query,
            records,
        )

        connection.commit()

    except Exception as error:

        connection.rollback()

        print("\nMySQL Error:")
        print(error)

        cursor.close()

        raise

    cursor.close()

    print(
        f"{len(records)} records processed successfully."
    )


def main():

    print("=" * 60)
    print("Incremental MySQL Order Loader")
    print("=" * 60)

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Processed file not found: {INPUT_FILE}"
        )

    df = pd.read_csv(
        INPUT_FILE,
        parse_dates=["order_date"],
    )

    print(
        f"\nRecords found in CSV : {len(df)}"
    )

    connection = get_connection()

    try:

        create_table(connection)

        load_orders(
            connection,
            df,
        )

    finally:

        connection.close()

    print(
        "\nDay 4 incremental loading completed successfully."
    )


if __name__ == "__main__":
    main()