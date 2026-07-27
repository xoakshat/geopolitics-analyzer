import plotly.express as px  # plotly.express is the easy, quick way to make charts
import plotly.graph_objects as go  # graph_objects gives more control for custom charts
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def chart_top_military_spenders(df_result, year):
    """
    Makes a horizontal bar chart of the top military spenders.
    Horizontal bar charts are great for comparing countries — labels don't overlap.
    """

    # px.bar() creates a bar chart
    # x = which column becomes the bar length
    # y = which column labels each bar
    # orientation="h" means horizontal
    # title = the chart title
    fig = px.bar(
        df_result,
        x="Military Spending (% GDP)",
        y="Country",
        orientation="h",
        title=f"Top military spenders as % of GDP ({year})",
        labels={"Military Spending (% GDP)": "% of GDP", "Country": ""},
        color="Military Spending (% GDP)",
        color_continuous_scale="Reds"  # higher spending = darker red
    )

    # Flip the Y axis so highest is at the top
    fig.update_layout(yaxis={"categoryorder": "total ascending"})

    # Save as an interactive HTML file — anyone can open this in a browser
    output_path = os.path.join("outputs", "charts", f"military_spenders_{year}.html")
    fig.write_html(output_path)
    print(f"Chart saved: {output_path}")

    return fig


def chart_gdp_trend(gdp_df):
    """
    Makes a line chart showing GDP over time for multiple countries.
    Each country gets its own colored line.
    """

    # Convert GDP from raw dollars to trillions for readability
    gdp_df = gdp_df.copy()
    gdp_df["GDP (Trillions USD)"] = gdp_df["amount"] / 1_000_000_000_000

    # px.line() creates a line chart
    # color="country_name" means each country gets a different colored line
    fig = px.line(
        gdp_df,
        x="year",
        y="GDP (Trillions USD)",
        color="country_name",
        title="GDP over time: India, China, United States",
        labels={"year": "Year", "country_name": "Country"},
        markers=True  # show dots at each data point
    )

    output_path = os.path.join("outputs", "charts", "gdp_trend.html")
    fig.write_html(output_path)
    print(f"Chart saved: {output_path}")

    return fig


def chart_military_vs_gdp(mvg_df, year):
    """
    Makes a scatter plot: X axis = GDP size, Y axis = military spending %.
    Countries in the top-left corner are relatively poor but spend a lot on military.
    Countries in the bottom-right are rich but spend little — or the opposite.
    """

    fig = px.scatter(
        mvg_df,
        x="gdp_trillions",
        y="mil_pct_gdp",
        text="country_name",  # show country names as labels on the dots
        title=f"Military spending vs economic size ({year})",
        labels={
            "gdp_trillions": "GDP (Trillions USD)",
            "mil_pct_gdp": "Military spending (% of GDP)"
        },
        size="gdp_trillions",  # bigger dot = bigger economy
        color="mil_pct_gdp",   # color by military spending intensity
        color_continuous_scale="Oranges"
    )

    # Move text labels so they don't overlap with the dots
    fig.update_traces(textposition="top center")

    output_path = os.path.join("outputs", "charts", f"military_vs_gdp_{year}.html")
    fig.write_html(output_path)
    print(f"Chart saved: {output_path}")

    return fig


if __name__ == "__main__":
    # Import and run the analyzer to get fresh data
    from analyzer import load_data, top_military_spenders, gdp_trend, military_vs_gdp

    print("Loading data...")
    df = load_data()

    print("Creating charts...")

    # Chart 1: Top military spenders
    top = top_military_spenders(df, year=2022)
    chart_top_military_spenders(top, year=2022)

    # Chart 2: GDP trend
    gdp = gdp_trend(df, countries=["India", "China", "United States"])
    chart_gdp_trend(gdp)

    # Chart 3: Military vs GDP scatter
    mvg = military_vs_gdp(df, year=2022)
    chart_military_vs_gdp(mvg, year=2022)

    print("\nAll charts created! Open outputs/charts/ to see them.")