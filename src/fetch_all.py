# This file uses the config to fetch data for ALL countries at once
import sys
import os

# This line lets Python find files in the parent folder
# When you run a file inside src/, Python doesn't know about the parent folder by default
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config  # import our settings file
from fetcher import fetch_world_bank_data, save_raw_data
from cleaner import clean_dataframe, save_to_database
import pandas as pd

def fetch_and_clean_all():
    """Fetch data for every country and indicator in our config."""

    # We'll collect all data into one big list, then combine it
    all_data = []

    # Loop through every country in our config
    # .items() gives us both the code ("IN") and the name ("India") at once
    for country_code, country_name in config.COUNTRIES.items():

        # Loop through every indicator
        for indicator_code, indicator_name in config.INDICATORS.items():

            # Fetch the data
            df = fetch_world_bank_data(
                country_code=country_code,
                indicator_code=indicator_code,
                start_year=config.START_YEAR,
                end_year=config.END_YEAR
            )

            if df is not None:
                # Clean it
                clean_df = clean_dataframe(df, indicator_name)

                if clean_df is not None:
                    all_data.append(clean_df)  # add to our list

    # Combine all dataframes into one big table
    # pd.concat() stacks multiple tables on top of each other
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        print(f"\nTotal rows collected: {len(combined)}")

        # Save to database as one unified table
        save_to_database(combined, table_name="all_data", db_path=config.DB_PATH)

        # Also save as CSV
        combined.to_csv("data/clean/all_data.csv", index=False)
        print("Saved combined data to data/clean/all_data.csv")

        return combined
    else:
        print("No data was collected.")
        return None

if __name__ == "__main__":
    fetch_and_clean_all()