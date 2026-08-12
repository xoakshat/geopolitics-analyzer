import sqlite3
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def load_data(db_path=config.DB_PATH):
    """Load all data from the database into a pandas dataframe."""
    conn = sqlite3.connect(db_path)

    
    df = pd.read_sql("SELECT * FROM all_data", conn)

    conn.close()
    return df


def top_military_spenders(df, year=2022, top_n=10):
    """
    Which countries spent the most on military as % of GDP in a given year?

    % of GDP means: for every 100 rupees the country produced, how many went to military?
    This is a fairer comparison than raw amount, because big economies spend more in absolute terms.
    """

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

def trade_balance_trend(df, countries=None):
    """
    Shows whether a country exports more than it imports over time.

    Trade balance = Exports minus Imports
    Positive number = surplus (country sells more than it buys) — generally good
    Negative number = deficit (country buys more than it sells)

    This is interesting for India because India runs a consistent trade deficit
    but its exports have grown dramatically over 20 years.
    """
    if countries is None:
        countries = ["India", "China", "United States"]

    # Get export rows for selected countries
    exports = df[
        (df["indicator"] == "NE.EXP.GNFS.CD") &
        (df["country_name"].isin(countries))
    ][["country_name", "year", "amount"]].rename(columns={"amount": "exports"})

    # Get import rows for selected countries
    imports = df[
        (df["indicator"] == "NE.IMP.GNFS.CD") &
        (df["country_name"].isin(countries))
    ][["country_name", "year", "amount"]].rename(columns={"amount": "imports"})

    # Merge the two tables — match each row by country AND year
    # inner join means: only keep rows where both export AND import data exists
    merged = pd.merge(exports, imports, on=["country_name", "year"], how="inner")

    # Calculate trade balance
    merged["trade_balance"] = merged["exports"] - merged["imports"]

    # Convert from raw USD to billions — easier to read
    # 1 billion = 1,000,000,000
    merged["exports_billions"]       = merged["exports"] / 1_000_000_000
    merged["imports_billions"]       = merged["imports"] / 1_000_000_000
    merged["trade_balance_billions"] = merged["trade_balance"] / 1_000_000_000

    # Sort by country name then year — cleanest order
    merged = merged.sort_values(["country_name", "year"]).reset_index(drop=True)

    return merged


def export_growth_rank(df, start_year=2000, end_year=2022):
    """
    Which country grew its exports the fastest from start_year to end_year?

    This tells you who became more economically powerful over time.
    China's export growth from 2000-2022 is one of the most dramatic
    economic stories of the 21st century — your data will show this.
    """
    # Filter: only export rows, only for the two years we're comparing
    exports = df[
        (df["indicator"] == "NE.EXP.GNFS.CD") &
        (df["year"].isin([start_year, end_year]))
    ]

    # pivot_table reshapes the data
    # Before: one row per (country, year)
    # After: one row per country, with columns for each year
    pivot = exports.pivot_table(
        index="country_name",
        columns="year",
        values="amount"
    ).reset_index()

    pivot.columns.name = None  # clean up the column header

    # Only keep rows where we have data for both years
    pivot = pivot.dropna(subset=[start_year, end_year])

    # Calculate % growth: ((new - old) / old) * 100
    pivot["growth_pct"] = (
        (pivot[end_year] - pivot[start_year]) / pivot[start_year]
    ) * 100

    # Convert to billions for readability
    pivot[f"{start_year}_billions"] = pivot[start_year] / 1_000_000_000
    pivot[f"{end_year}_billions"]   = pivot[end_year]   / 1_000_000_000

    # Sort highest growth first
    result = pivot[["country_name", f"{start_year}_billions", f"{end_year}_billions", "growth_pct"]]
    result = result.sort_values("growth_pct", ascending=False).reset_index(drop=True)

    return result