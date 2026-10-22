
from pathlib import Path
from getpass import getpass

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# Find the cleaned CSV folder
possible_paths = [
    Path("data/processed"),
    Path("venv/data/processed"),
]

data_dir = next(
    (p for p in possible_paths if p.is_dir()
     and len(list(p.glob("*.csv"))) == 9),
    None
)

if data_dir is None:
    raise FileNotFoundError(
        "Could not find all 9 CSV files in data/processed "
        "or venv/data/processed."
    )

print("CSV folder:", data_dir.resolve())

password = getpass("Enter PostgreSQL password for postgres: ")

url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password=password,
    host="localhost",
    port=5432,
    database="netflix_intelligence",
)

engine = create_engine(url)

tables = [
    "subscription_plans",
    "customers",
    "content",
    "subscriptions",
    "viewing_activity",
    "payments",
    "support_tickets",
    "customer_feedback",
    "churn_labels",
]

try:
    with engine.connect() as conn:
        print("PostgreSQL connection successful.")

    for table in tables:
        file_path = data_dir / f"{table}.csv"
        df = pd.read_csv(file_path, low_memory=False)

        # Convert known date columns safely
        for column in df.columns:
            if column.endswith("_date"):
                df[column] = pd.to_datetime(
                    df[column], errors="coerce"
                )

        # Do not overwrite existing tables
        df.to_sql(
            table,
            engine,
            if_exists="fail",
            index=False,
            chunksize=1000,
            method="multi",
        )

        print(f"Imported {table}: {len(df)} rows")

    print("\nAll 9 CSV files imported successfully!")

except Exception as error:
    print("\nImport stopped:", error)
    print("Check which tables were imported before retrying.")

finally:
    engine.dispose()
