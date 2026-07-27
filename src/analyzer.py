import sqlite3
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def load_data(db_path=config.DB_PATH):
    """Load all data from the database into a pandas dataframe."""
    conn = sqlite3.connect(db_path)

    # pd.read_sql reads a SQL query and gives us back a dataframe
    # SQL is a language for asking questions of a database
    # SELECT * FROM all_data means "give me every column from the all_data table"
    df = pd.read_sql("SELECT * FROM all_data", conn)

    conn.close()
    return df


def top_military_spenders(df, year=2022, top_n=10):
    """
    Which countries spent the most on military as % of GDP in a given year?
    
    % of GDP means: for every 100 rupees the country produced, how many went to military?
    This is a fairer comparison than raw amount, because big economies spend more in absolute terms.
    """
    # Filter: only military spending rows, only for the given year
    mil = df[
        (df["indicator"] == "MS.MIL.XPND.GD.ZS") &
        (df["year"] == year)
    ]

    # Sort from highest to lowest, take top N
    top = mil.sort_values("amount", ascending=False).head(top_n)

    # Keep only the columns we want to display
    result = top[["country_name", "year", "amount", "indicator_name"]].copy()
    result.columns = ["Country", "Year", "Military Spending (% GDP)", "Indicator"]
    result = result.reset_index(drop=True)

    return result


def gdp_trend(df, countries=None):
    """
    How has GDP changed over time for a list of countries?
    Good for making a line chart — one line per country.
    """
    if countries is None:
        countries = ["India", "China", "United States"]

    # Filter: only GDP rows, only for the selected countries
    gdp = df[
        (df["indicator"] == "NY.GDP.MKTP.CD") &
        (df["country_name"].isin(countries))
    ]

    # isin() checks if a value is inside a list
    # Like asking: "is country_name one of these three countries?"

    # Sort by year
    gdp = gdp.sort_values(["country_name", "year"])

    return gdp[["country_name", "year", "amount"]]


def military_vs_gdp(df, year=2022):
    """
    Compare military spending vs GDP for each country in one year.
    Useful for finding countries that punch above their weight militarily.
    """
    # Get military spending for the year
    mil = df[
        (df["indicator"] == "MS.MIL.XPND.GD.ZS") &
        (df["year"] == year)
    ][["country_name", "amount"]].rename(columns={"amount": "mil_pct_gdp"})

    # Get GDP for the year
    gdp = df[
        (df["indicator"] == "NY.GDP.MKTP.CD") &
        (df["year"] == year)
    ][["country_name", "amount"]].rename(columns={"amount": "gdp_usd"})

    # Merge the two tables on country_name
    # merge() is like doing a VLOOKUP in Excel — it matches rows from two tables
    combined = pd.merge(mil, gdp, on="country_name", how="inner")

    # Convert GDP to trillions for readability
    combined["gdp_trillions"] = combined["gdp_usd"] / 1_000_000_000_000
    combined = combined.sort_values("mil_pct_gdp", ascending=False)

    return combined[["country_name", "mil_pct_gdp", "gdp_trillions"]]


if __name__ == "__main__":
    # Load all data
    print("Loading data...")
    df = load_data()
    print(f"Loaded {len(df)} rows.")

    # Run analysis 1
    print("\n--- Top Military Spenders in 2022 ---")
    top_spenders = top_military_spenders(df, year=2022)
    print(top_spenders.to_string(index=False))

    # Run analysis 2
    print("\n--- GDP Trend: India, China, USA ---")
    gdp = gdp_trend(df, countries=["India", "China", "United States"])
    print(gdp.tail(10).to_string(index=False))

    # Run analysis 3
    print("\n--- Military Spending vs GDP (2022) ---")
    mvg = military_vs_gdp(df, year=2022)
    print(mvg.to_string(index=False))