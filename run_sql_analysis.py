
from pathlib import Path
import getpass
import psycopg2

sql_file = Path("database/01_customer_analysis.sql")

if not sql_file.exists():
    print("SQL file not found:", sql_file.resolve())
    raise SystemExit(1)

sql_text = sql_file.read_text(encoding="utf-8")

# Split the file into individual SQL statements.
statements = [
    statement.strip()
    for statement in sql_text.split(";")
    if statement.strip()
]

try:
    connection = psycopg2.connect(
        host="localhost",
        database="netflix_intelligence",
        user="postgres",
        password=getpass.getpass("PostgreSQL password: "),
    )

    connection.autocommit = True

    with connection.cursor() as cursor:
        for number, statement in enumerate(statements, start=1):
            print(f"\n{'=' * 50}")
            print(f"QUERY {number}")
            print(statement)

            try:
                cursor.execute(statement)

                if cursor.description:
                    columns = [item[0] for item in cursor.description]
                    rows = cursor.fetchall()

                    print("\nColumns:", " | ".join(columns))
                    for row in rows[:30]:
                        print(row)

                    if len(rows) > 30:
                        print(f"... plus {len(rows) - 30} more rows")
                else:
                    print("Query completed successfully.")

            except Exception as error:
                print("Query failed:", error)

    connection.close()
    print("\nSQL analysis finished.")

except Exception as error:
    print("Database connection failed:", error)
