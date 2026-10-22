import pandas as pd
import os

folder = "data/raw"

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
    path = os.path.join(folder, file)

    print("\n" + "=" * 60)
    print(f"FILE: {file}")
    print("=" * 60)

    if os.path.exists(path):
        df = pd.read_csv(path)

        print("Rows:", len(df))
        print("Columns:", len(df.columns))
        print("\nColumn Names:")
        print(list(df.columns))

        print("\nMissing Values:")
        print(df.isnull().sum())

        print("\nDuplicate Rows:", df.duplicated().sum())

    else:
        print("FILE NOT FOUND:", path)

print("\nData checking completed.")