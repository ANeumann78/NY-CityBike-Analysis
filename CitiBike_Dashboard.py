import streamlit as st
import pandas as pd
from pathlib import Path
import streamlit.components.v1 as components

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------------- App Configuration ----------------
st.set_page_config(page_title="NYC CitiBike Dashboard", layout="wide")

DATA_FILE = "citibike_sample_1.parquet"
DEFAULT_MAP_HTML = "top_50_stop_and_end_stations_heat.html"  

BG = "#0E1117"
GRID = "rgba(255,255,255,0.08)"
FONT = "rgba(255,255,255,0.92)"


# ---------------- Helpers ----------------
@st.cache_data(show_spinner=False)
def load_df(path: str) -> pd.DataFrame:
    return pd.read_parquet(path)

def apply_plotly_dark(fig, *, height=560, margin=None):
    if margin is None:
        margin = dict(l=70, r=70, t=95, b=55)
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor=BG,
        plot_bgcolor=BG,
        height=height,
        margin=margin,
        title=dict(x=0.5, y=0.95, font=dict(size=20, color=FONT)),
        font=dict(size=12, color=FONT),
        hovermode="x unified",
    )
    fig.update_xaxes(gridcolor=GRID, zeroline=False)
    fig.update_yaxes(gridcolor=GRID, zeroline=False)
    return fig

def embed_html(path: str, height: int = 740):
    p = Path(path)
    if not p.exists():
        st.error(f"Map file not found: {path}")
        st.info("Put the HTML map in the same folder as this script, or update DEFAULT_MAP_HTML.")
        return
    components.html(p.read_text(encoding="utf-8"), height=height, scrolling=True)

def month_to_season(m: int) -> str:
    if m in (12, 1, 2): return "winter"
    if m in (3, 4, 5):  return "spring"
    if m in (6, 7, 8):  return "summer"
    return "fall"


#---------------- Load Data ----------------
if not Path(DATA_FILE).exists():
    st.error(f"Missing data file: {DATA_FILE}")
    st.stop()

df = load_df(DATA_FILE).copy()
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])

#Sidebar controls
st.sidebar.header("Controls")
min_d, max_d = df["date"].min().date(), df["date"].max().date()
start_date, end_date = st.sidebar.date_input(
    "Date range",
    value=(min_d, max_d),
    min_value=min_d,
    max_value=max_d,
)

df_f = df[(df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)].copy()

pages = [
    "Intro",
    "Daily Trips vs Temperature",
    "Most Popular Stations",
    "Interactive Map",
    "Extra Insight (Seasonality)",
    "Recommendations",
]
page = st.sidebar.selectbox("Pages", pages)


# ---------------- Intro ----------------
if page == "Intro":
    st.title("NYC CitiBike Dashboard 🚲🗽")
    st.markdown("""
This dashboard summarizes CitiBike demand patterns and highlights implications for NYC’s bike **supply and rebalancing** problem.

Use the sidebar pages to explore:
- Demand vs temperature (dual-axis)
- Most popular start stations
- Interactive map (HTML embed)
- Seasonality insight
- Final recommendations
""")

    c1, c2, c3 = st.columns(3)
    c1.metric("Rows in sample (filtered)", f"{len(df_f):,}")
    c2.metric("Trips (sum)", f"{int(df_f['trips'].sum()):,}")
    c3.metric("Unique start stations", f"{df_f['start_station_id'].nunique():,}")

    st.caption("Data source: reduced sample parquet for fast dashboard performance.")
    st.info("Tip: Adjust the date range in the sidebar to see how patterns shift over time.")


# ---------------- Dual-axis Line Chart ----------------
elif page == "Daily Trips vs Temperature":
    st.title("Daily Bike Trips vs Temperature")

    daily = (
        df_f.assign(day=df_f["date"].dt.date)
           .groupby("day", as_index=False)
           .agg(trips=("trips", "sum"), avgTemp=("avgTemp", "mean"))
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=daily["day"],
            y=daily["trips"],
            name="Daily Bike Trips",
            mode="lines",
            line=dict(color="#00E5FF", width=2),
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=daily["day"],
            y=daily["avgTemp"],
            name="Average Temperature (°C)",
            mode="lines",
            line=dict(color="#FFA726", width=2, dash="dot"),
        ),
        secondary_y=True,
    )

    fig.update_layout(title="Daily Bike Trips vs. Temperature in NYC")
    fig.update_yaxes(title_text="Number of Trips", secondary_y=False, tickformat=",")
    fig.update_yaxes(title_text="Temperature (°C)", secondary_y=True, showgrid=False)
    fig.update_xaxes(title_text="Date")

    apply_plotly_dark(fig, height=560)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Interpretation**
- Trips generally rise as temperatures warm and fall as temperatures cool, indicating strong weather seasonality.
- Daily noise remains high even at similar temperatures, pointing to additional demand drivers (weekday/weekend, rain, holidays, events).
- Temperature is useful as a baseline forecasting feature for bike supply and rebalancing, but operational planning should also incorporate calendar and weather factors.
""")


# ---------------- Most Popular Stations ----------------
elif page == "Most Popular Stations":
    st.title("Top Start Stations")

    top_n = st.slider("Top N stations", 10, 50, 20, 5)

    top = (
        df_f.groupby(["start_station_id", "start_station_name"], as_index=False)
            .agg(trips=("trips", "sum"))
            .sort_values("trips", ascending=False)
            .head(top_n)
            .sort_values("trips")
    )

    fig = px.bar(
        top,
        x="trips",
        y="start_station_name",
        orientation="h",
        title=f"Top {top_n} Most Popular Start Stations",
        labels={"trips": "Number of Trips", "start_station_name": "Start Station"},
        color="trips",
        color_continuous_scale="Blues",
    )

    apply_plotly_dark(fig, height=700, margin=dict(l=260, r=60, t=95, b=55))
    fig.update_xaxes(tickformat=",")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Interpretation**
- Demand is concentrated: a small set of stations generates a large share of trips.
- These high-volume hubs are prime targets for proactive rebalancing to prevent stations from going empty.
- Tracking these stations over time helps identify predictable supply pressure points.
""")


# ---------------- Map Page ----------------
elif page == "Interactive Map":
    st.title("Interactive Map")

    html_files = sorted([p.name for p in Path(".").glob("*.html")])
    if not html_files:
        st.error("No .html map files found in this folder. Add your exported map HTML here.")
        st.stop()

    default_idx = html_files.index(DEFAULT_MAP_HTML) if DEFAULT_MAP_HTML in html_files else 0
    chosen = st.selectbox("Choose map", html_files, index=default_idx)

    embed_html(chosen, height=740)

    st.markdown("""
**Interpretation**
- The map highlights where CitiBike activity concentrates (hotspots) and/or which flows dominate (depending on the chosen map).
- Spatial clustering reveals areas most likely to experience bike shortages or dock saturation.
- These patterns support a zone-based rebalancing strategy: prioritize high-impact corridors rather than reacting station-by-station.
""")


# ---------------- Extra Insight ----------------
elif page == "Extra Insight (Seasonality)":
    st.title("Extra Insight: Seasonal Demand")

    d = df_f.copy()
    d["season"] = d["date"].dt.month.map(month_to_season)

    season_order = ["winter", "spring", "summer", "fall"]
    d["season"] = pd.Categorical(d["season"], categories=season_order, ordered=True)

    seasonal = (
        d.groupby("season", as_index=False)
         .agg(trips=("trips", "sum"), avgTemp=("avgTemp", "mean"))
         .sort_values("season")
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(x=seasonal["season"], y=seasonal["trips"], name="Total Trips",
               marker=dict(color="#00E5FF"), opacity=0.9),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=seasonal["season"], y=seasonal["avgTemp"], name="Average Temperature (°C)",
                   mode="lines+markers", line=dict(color="#FFA726", width=3),
                   marker=dict(size=8)),
        secondary_y=True,
    )

    fig.update_layout(title="Seasonal CitiBike Demand vs Temperature")
    fig.update_yaxes(title_text="Total Trips", secondary_y=False, tickformat=",")
    fig.update_yaxes(title_text="Average Temperature (°C)", secondary_y=True, showgrid=False)
    fig.update_xaxes(title_text="Season", showgrid=False)

    apply_plotly_dark(fig, height=560)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
**Interpretation**
- Demand peaks in warmer seasons and falls in colder ones, reinforcing temperature as a major demand driver.
- Operational capacity and rebalancing effort should scale up in spring/summer and adjust downward in winter.
""")


# ---------------- Recommendations ----------------
elif page == "Recommendations":
    st.title("Recommendations")

    st.markdown("""
### Recommendations to reduce supply imbalance

1. **Prioritize top start-station hubs**
   - Monitor and proactively rebalance around the busiest stations, especially during commuting windows.
   - These hubs are recurring sources of station-level imbalance.

2. **Use weather-aware demand planning**
   - Temperature is a strong baseline demand signal.
   - Add day-of-week and precipitation to forecast demand spikes and pre-position bikes before shortages occur.

3. **Seasonal operations strategy**
   - Increase rebalancing capacity and bike availability in spring/summer when demand ramps up.
   - Shift focus to efficiency and maintenance planning in winter.

4. **Zone-based rebalancing from map patterns**
   - Use hotspot corridors and repeated flows to define rebalancing zones instead of reacting station-by-station.

### Next steps
- Add precipitation/wind, holidays, and member-vs-casual segmentation to better explain daily variability.
- Quantify “imbalance” directly if dock availability data is available (empty/full station events).
""")