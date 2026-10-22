import pandas as pd
import os

RAW = "data/raw"
PROCESSED = "data/processed"

os.makedirs(PROCESSED, exist_ok=True)

files = [
    "customers.csv",
    "subscription_plans.csv",
    "subscriptions.csv",
    "content.csv",
    "viewing_activity.csv",
    "payments.csv",
    "support_tickets.csv",
    "customer_feedback.csv",
    "churn_labels.csv"
]

for file in files:

    input_path = os.path.join(RAW, file)
    output_path = os.path.join(PROCESSED, file)

    print(f"Cleaning: {file}")

    df = pd.read_csv(input_path)

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Remove leading/trailing spaces from text columns
    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].astype(str).str.strip()

    # Save cleaned file
    df.to_csv(output_path, index=False)

    print(f"Saved: {output_path}")
    print(f"Rows: {len(df)}")
    print()

print("================================")
print("DATA CLEANING COMPLETED")
print("================================")