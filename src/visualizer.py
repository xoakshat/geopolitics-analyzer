import plotly.express as px
import plotly.graph_objects as go
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def chart_top_military_spenders(df_result, year):
    """
    Makes a horizontal bar chart of the top military spenders.
    """

    fig = px.bar(
        df_result,
        x="Military Spending (% GDP)",
        y="Country",
        orientation="h",
        title=f"Top military spenders as % of GDP ({year})",
        labels={
            "Military Spending (% GDP)": "% of GDP",
            "Country": ""
        },
        color="Military Spending (% GDP)",
        color_continuous_scale="Reds"
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    output_path = os.path.join(
        "outputs",
        "charts",
        f"military_spenders_{year}.html"
    )

    fig.write_html(output_path)
    print(f"Chart saved: {output_path}")

    return fig


def chart_gdp_trend(gdp_df):
    """
    Makes a line chart showing GDP over time for multiple countries.
    """

    gdp_df = gdp_df.copy()

    gdp_df["GDP (Trillions USD)"] = (
        gdp_df["amount"] / 1_000_000_000_000
    )

    fig = px.line(
        gdp_df,
        x="year",
        y="GDP (Trillions USD)",
        color="country_name",
        title="GDP over time: India, China, United States",
        labels={
            "year": "Year",
            "country_name": "Country"
        },
        markers=True
    )

    output_path = os.path.join(
        "outputs",
        "charts",
        "gdp_trend.html"
    )

    fig.write_html(output_path)
    print(f"Chart saved: {output_path}")

    return fig


def chart_military_vs_gdp(mvg_df, year):
    """
    Makes a scatter plot comparing GDP size
    with military spending as % of GDP.
    """

    fig = px.scatter(
        mvg_df,
        x="gdp_trillions",
        y="mil_pct_gdp",
        text="country_name",
        title=f"Military spending vs economic size ({year})",
        labels={
            "gdp_trillions": "GDP (Trillions USD)",
            "mil_pct_gdp": "Military spending (% of GDP)"
        },
        size="gdp_trillions",
        color="mil_pct_gdp",
        color_continuous_scale="Oranges"
    )

    fig.update_traces(
        textposition="top center"
    )

    output_path = os.path.join(
        "outputs",
        "charts",
        f"military_vs_gdp_{year}.html"
    )

    fig.write_html(output_path)
    print(f"Chart saved: {output_path}")

    return fig


def chart_trade_balance(trade_df):
    """
    Line chart showing trade balance over time for multiple countries.

    Above zero = surplus.
    Below zero = deficit.
    """

    fig = px.line(
        trade_df,
        x="year",
        y="trade_balance_billions",
        color="country_name",
        title="Trade balance over time — Exports minus Imports (USD Billions)",
        labels={
            "trade_balance_billions": "Trade Balance (Billions USD)",
            "year": "Year",
            "country_name": "Country"
        },
        markers=True
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray",
        annotation_text="Break-even (zero balance)"
    )

    output_path = "outputs/charts/trade_balance.html"

    fig.write_html(output_path)

    print(f"Saved → {output_path}")

    return fig


def chart_export_growth(growth_df, start_year, end_year):
    """
    Horizontal bar chart showing which country's
    exports grew the fastest.
    """

    fig = px.bar(
        growth_df,
        x="growth_pct",
        y="country_name",
        orientation="h",
        title=f"Export growth by country ({start_year}–{end_year})",
        labels={
            "growth_pct": "Export growth (%)",
            "country_name": ""
        },
        color="growth_pct",
        color_continuous_scale="Blues"
    )

    fig.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    output_path = (
        f"outputs/charts/export_growth_{start_year}_{end_year}.html"
    )

    fig.write_html(output_path)

    print(f"Saved → {output_path}")

    return fig


def chart_india_exports_imports(trade_df):
    """
    Special chart just for India — shows exports
    and imports on the same chart.
    """

    india = trade_df[
        trade_df["country_name"] == "India"
    ].copy()

    india_melted = india.melt(
        id_vars="year",
        value_vars=[
            "exports_billions",
            "imports_billions"
        ],
        var_name="Type",
        value_name="USD Billions"
    )

    india_melted["Type"] = india_melted["Type"].map({
        "exports_billions": "Exports",
        "imports_billions": "Imports"
    })

    fig = px.line(
        india_melted,
        x="year",
        y="USD Billions",
        color="Type",
        title="India: Exports vs Imports over time (USD Billions)",
        labels={
            "year": "Year"
        },
        markers=True,
        color_discrete_map={
            "Exports": "#2196F3",
            "Imports": "#E63946"
        }
    )

    output_path = "outputs/charts/india_exports_vs_imports.html"

    fig.write_html(output_path)

    print(f"Saved → {output_path}")

    return fig


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    from analyzer import (
    load_data,
    top_military_spenders,
    gdp_trend,
    military_vs_gdp,
    trade_balance_trend,
    export_growth_rank
)

    print("Loading data...")

    df = load_data()

    print("Creating charts...")

    # Chart 1: Top military spenders
    top = top_military_spenders(
        df,
        year=2022
    )

    chart_top_military_spenders(
        top,
        year=2022
    )

    # Chart 2: GDP trend
    gdp = gdp_trend(
        df,
        countries=[
            "India",
            "China",
            "United States"
        ]
    )

    chart_gdp_trend(gdp)

    # Chart 3: Military vs GDP scatter
    mvg = military_vs_gdp(
        df,
        year=2022
    )

    chart_military_vs_gdp(
    mvg,
    year=2022
)


# Chart 4: Trade balance
print("\nRunning trade balance analysis...")

trade = trade_balance_trend(
    df,
    countries=["India", "China", "United States"]
)

chart_trade_balance(trade)


# Chart 5: Export growth
print("\nRunning export growth ranking...")

growth = export_growth_rank(
    df,
    start_year=2000,
    end_year=2022
)

chart_export_growth(
    growth,
    2000,
    2022
)


# Chart 6: India exports vs imports
chart_india_exports_imports(trade)


print(
    "\nAll charts created! "
    "Open outputs/charts/ to see them."
)