# Geopolitics Data Analyzer

A Python tool that automatically fetches real economic and military data 
for 10 countries from the World Bank API, stores it in a structured 
database, and generates interactive charts.

## What it analyzes
- Military spending as % of GDP (2000–2023)
- GDP growth trajectories across major economies
- Cross-country comparisons: India, China, USA, Russia, and more

## Charts produced
- Top military spenders (interactive bar chart)
- GDP trend over time (interactive line chart)  
- Military spending vs economic size (scatter plot)

## Tech stack
- Python 3.11
- pandas — data cleaning and analysis
- plotly — interactive charts
- SQLite — local database storage
- requests — API calls

## How to run it

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `python main.py`

Charts will appear in `outputs/charts/` as interactive HTML files.

## Data sources
- [World Bank Open Data](https://data.worldbank.org/) — GDP, military spending
- Data covers 10 countries from 2000 to 2023

## Built by
<Akshat Tiwari> — BCA student with an interest in data and geopolitics.