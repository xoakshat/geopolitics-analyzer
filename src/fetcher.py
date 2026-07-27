# We import two libraries we installed earlier
import requests   # this lets us talk to the internet
import pandas as pd  # 'pd' is just a short nickname for pandas — everyone uses this
import os  # this lets us work with files and folders on your computer

def fetch_world_bank_data(country_code, indicator_code, start_year=2000, end_year=2023):
    """
    This is a function. Think of a function as a mini-program inside your program.
    You give it inputs (country_code, indicator_code, years),
    it does some work, and gives you back an output (the data).

    country_code: a 2-letter code like "IN" for India, "CN" for China, "US" for USA
    indicator_code: a code for what data you want
        - NY.GDP.MKTP.CD = GDP in US dollars
        - MS.MIL.XPND.GD.ZS = Military spending as % of GDP
    """

    # This is the URL (web address) of the World Bank API
    # An API is like a restaurant menu — you ask for something specific, it gives it to you
    # We build the URL by putting the country and indicator code inside it
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}"

    # These are extra options we send with our request
    # 'format': 'json' means "give us data in JSON format" (JSON is like a structured dictionary)
    # 'per_page': 100 means "give us up to 100 rows of data"
    # 'mrv': end_year - start_year means "most recent values going back this many years"
    params = {
        "format": "json",
        "per_page": 100,
        "date": f"{start_year}:{end_year}"
    }

    # This line actually goes to the internet and fetches the data
    # It's like typing the URL into your browser and pressing Enter, but in code
    print(f"Fetching data for {country_code} - {indicator_code}...")
    response = requests.get(url, params=params)

    # The API sends back data. We need to check if it worked.
    # Status code 200 means "success" — like a green light
    if response.status_code != 200:
        print(f"Error! Could not fetch data. Status code: {response.status_code}")
        return None  # return None means "give back nothing, something went wrong"

    # The response comes as JSON — we convert it to a Python list
    # JSON looks like: [{"value": 123, "date": "2022"}, ...]
    data = response.json()

    # The World Bank API always returns 2 things:
    # data[0] is metadata (information about the request — ignore this)
    # data[1] is the actual records we want
    if len(data) < 2 or data[1] is None:
        print(f"No data found for {country_code} - {indicator_code}")
        return None

    records = data[1]  # this is a list of dictionaries

    # Now we turn the raw API response into a clean, readable table using pandas
    # pd.DataFrame() turns a list of dictionaries into a table (like Excel)
    df = pd.DataFrame(records)

    # The API returns many columns we don't need. We keep only the useful ones:
    # 'date' = the year
    # 'value' = the number we care about (e.g. GDP amount)
    # 'country' = a nested dictionary with the country name inside it
    df = df[["date", "value", "country"]]

    # The 'country' column contains a dictionary like {"id": "IN", "value": "India"}
    # We only want the name "India", so we extract it like this:
    df["country_name"] = df["country"].apply(lambda x: x["value"])

    # We also add the indicator code so we remember what this data represents
    df["indicator"] = indicator_code

    # Now drop the original 'country' column since we extracted the name
    df = df.drop(columns=["country"])

    # Rename columns to be more readable
    df = df.rename(columns={"date": "year", "value": "amount"})

    print(f"Successfully fetched {len(df)} rows of data.")
    return df  # send the table back to whoever called this function


def save_raw_data(df, filename):
    """
    Saves the data to a CSV file.
    CSV means "Comma Separated Values" — it's a plain text file that Excel can open.
    Every row is one year of data. Columns are separated by commas.
    """
    if df is None:
        print("Nothing to save — dataframe is empty.")
        return

    # Build the full path to where we want to save the file
    filepath = os.path.join("data", "raw", filename)

    # Save it! index=False means "don't write row numbers in the file"
    df.to_csv(filepath, index=False)
    print(f"Saved to {filepath}")


# This block only runs when you run THIS file directly
# It won't run if another file imports this file — that's the point of this check
if __name__ == "__main__":

    # Let's test it with India's GDP data
    df = fetch_world_bank_data(
        country_code="IN",
        indicator_code="NY.GDP.MKTP.CD",
        start_year=2000,
        end_year=2023
    )

    # Save it
    save_raw_data(df, "india_gdp_raw.csv")

    # Let's also see what the data looks like by printing the first 5 rows
    if df is not None:
        print("\nHere is a preview of the data:")
        print(df.head())  # .head() shows the first 5 rows