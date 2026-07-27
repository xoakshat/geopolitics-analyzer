import pandas as pd
import sqlite3  # built into Python — no need to install
import os

def clean_dataframe(df, indicator_name):
    """
    Takes raw messy data and makes it clean and usable.
    
    df: the raw dataframe (table) from the fetcher
    indicator_name: a human-readable name like "GDP (USD)" or "Military Spending (% GDP)"
    """
    if df is None:
        return None

    # Make a copy so we don't modify the original data
    # This is good practice — always keep your raw data untouched
    clean = df.copy()

    # Convert year from string to integer
    # The API gives us year as "2022" (text), but we want 2022 (number) so we can sort and filter
    clean["year"] = pd.to_numeric(clean["year"], errors="coerce")
    # errors="coerce" means: if something can't be converted to a number, put NaN (empty) instead

    # Convert amount to float (a decimal number)
    # Some values come as strings or are missing — pd.to_numeric handles both
    clean["amount"] = pd.to_numeric(clean["amount"], errors="coerce")

    # Remove rows where 'amount' is NaN (missing)
    # NaN means "Not a Number" — it appears when there's no data for that year
    before_count = len(clean)  # how many rows before removing
    clean = clean.dropna(subset=["amount"])  # drop rows where 'amount' is missing
    after_count = len(clean)
    removed = before_count - after_count
    print(f"Removed {removed} rows with missing data. {after_count} rows remaining.")

    # Add a readable indicator name so we know what this data means
    clean["indicator_name"] = indicator_name

    # Sort by year so the data is in order (oldest first)
    clean = clean.sort_values("year", ascending=True)

    # Reset the index (row numbers) so they start from 0 again after dropping rows
    clean = clean.reset_index(drop=True)

    return clean


def save_to_database(df, table_name, db_path="data/geopolitics.db"):
    """
    Saves clean data to a SQLite database.
    
    SQLite is like a mini-Excel file. One file can hold many tables.
    table_name: what to call this table (like a sheet name in Excel)
    db_path: where to save the database file
    """
    if df is None:
        return

    # Connect to the database
    # If the file doesn't exist yet, SQLite creates it automatically
    # Think of this as "opening" the database
    conn = sqlite3.connect(db_path)

    # Save the dataframe to the database as a table
    # if_exists="replace" means: if this table already exists, overwrite it
    # index=False means: don't save row numbers as a column
    df.to_sql(table_name, conn, if_exists="replace", index=False)

    print(f"Saved {len(df)} rows to table '{table_name}' in {db_path}")

    # Always close the connection when you're done
    # Like closing a file — good practice so nothing gets corrupted
    conn.close()


def save_clean_csv(df, filename):
    """Also save a clean CSV file in case someone wants to open it in Excel."""
    if df is None:
        return
    filepath = os.path.join("data", "clean", filename)
    df.to_csv(filepath, index=False)
    print(f"Clean CSV saved to {filepath}")


if __name__ == "__main__":
    # Test: load the raw CSV we saved earlier, clean it, save it
    
    # Read the raw CSV file we created with fetcher.py
    raw_df = pd.read_csv("data/raw/india_gdp_raw.csv")
    print(f"Loaded {len(raw_df)} raw rows.")
    print("Raw data preview:")
    print(raw_df.head())

    # Clean it
    clean_df = clean_dataframe(raw_df, indicator_name="GDP (current USD)")

    # Save to database
    save_to_database(clean_df, table_name="gdp_data")

    # Also save a clean CSV
    save_clean_csv(clean_df, "india_gdp_clean.csv")

    print("\nClean data preview:")
    print(clean_df.head())