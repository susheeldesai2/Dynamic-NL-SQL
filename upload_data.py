import pandas as pd
import sqlite3
import os


def upload_csv_to_sqlite(csv_path, db_name="user_uploaded.db"):
    """Uploads a CSV file, extracts schema, and creates a dynamic SQLite table."""
    
    # Step 1: Read CSV into Pandas
    if not os.path.exists(csv_path):
        print(f"Error: The file {csv_path} does not exist.")
        return
    
    df = pd.read_csv(csv_path)
    
    if df.empty:
        print("Error: The CSV file is empty.")
        return

    # Step 2: Connect to SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Extract table name from filename (without extension)
    table_name = os.path.splitext(os.path.basename(csv_path))[0]

    # Step 3: Generate dynamic CREATE TABLE statement
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    
    for column in df.columns:
        col_type = "TEXT"  # Default to TEXT
        sample_value = df[column].dropna().iloc[0] if not df[column].dropna().empty else None
        
        if sample_value is not None:
            if isinstance(sample_value, int):
                col_type = "INTEGER"
            elif isinstance(sample_value, float):
                col_type = "REAL"

        create_table_query += f"{column.replace(' ', '_')} {col_type}, "
    
    create_table_query = create_table_query.rstrip(", ") + ")"  # Remove trailing comma

    # Step 4: Execute the table creation
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")  # Ensure a fresh table
    cursor.execute(create_table_query)
    conn.commit()

    # Step 5: Insert CSV data into the table
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.commit()

    print(f"Successfully uploaded CSV and created table: {table_name}")

    return table_name, db_name  # Return table name and database path for querying later

if __name__ == "__main__":
    csv_path = input("Enter path to the CSV file: ").strip()
    upload_csv_to_sqlite(csv_path)
