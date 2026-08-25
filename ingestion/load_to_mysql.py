from pathlib import Path

import pandas as pd

from ingestion.database import get_connection


INPUT_FILE = Path(
    "data/processed/orders_clean.csv"
)


def create_table(connection):
    cursor = connection.cursor()

    create_table_query = """
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
        total_amount DECIMAL(14, 2)
    )
    """

    cursor.execute(create_table_query)

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
        total_amount = VALUES(total_amount)
    """

    records = []

    for _, row in df.iterrows():
        records.append(
            (
                row["order_id"],
                row["customer_id"],
                row["customer_name"],
                row["product"],
                row["category"],
                int(row["quantity"]),
                float(row["unit_price"]),
                row["order_date"].date(),
                row["city"],
                row["country"],
                float(row["total_amount"]),
            )
        )

    cursor.executemany(
        insert_query,
        records,
    )

    connection.commit()

    cursor.close()

    print(
        f"{len(records)} records loaded into MySQL."
    )


def main():
    print("=" * 60)
    print("Cloud ELT Data Warehouse - MySQL Loader")
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
        f"\nProcessed rows : {len(df)}"
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
        "\nDay 3 MySQL loading completed successfully."
    )


if __name__ == "__main__":
    main()