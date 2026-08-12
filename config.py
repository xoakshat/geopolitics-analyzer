# config.py — all settings in one place

# Countries to analyze
# These are ISO 2-letter country codes used by the World Bank
COUNTRIES = {
    "IN": "India",
    "CN": "China",
    "US": "United States",
    "PK": "Pakistan",
    "RU": "Russia",
    "GB": "United Kingdom",
    "FR": "France",
    "DE": "Germany",
    "SA": "Saudi Arabia",
    "IL": "Israel"
}

# Years to fetch data for
START_YEAR = 2000
END_YEAR = 2023

# World Bank indicator codes
# These are like product codes — each one means a specific measurement
INDICATORS = {
    "NY.GDP.MKTP.CD": "GDP (current USD)",
    "MS.MIL.XPND.GD.ZS": "Military spending (% of GDP)",
    "SP.POP.TOTL": "Population",
    "NY.GDP.PCAP.CD": "GDP per capita (USD)",

    "NE.EXP.GNFS.CD": "Exports of goods and services (USD)",
    "NE.IMP.GNFS.CD": "Imports of goods and services (USD)",
    "TX.VAL.MRCH.CD.WT": "Merchandise exports (USD)",
    "TM.VAL.MRCH.CD.WT": "Merchandise imports (USD)",
    "BN.CAB.XOKA.CD": "Current account balance (USD)",
}

# Database path
DB_PATH = "data/geopolitics.db"