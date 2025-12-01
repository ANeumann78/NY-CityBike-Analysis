import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page Configuration 
# ----------------------------
st.set_page_config(
    page_title="NYC CitiBike Analysis Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Title & Description
# ----------------------------
st.title("🚲 NYC CitiBike Analysis Dashboard")
st.markdown(
    """
    Welcome to the **NYC CitiBike Analysis Dashboard**!

    This dashboard provides interactive visual insights into:
    - Bike trip patterns across New York City  
    - Popular stations and trip flows  
    - Weather relationships  
    - Interactive geospatial visualizations  
    - Aggregated metrics and trends  

    Use the sidebar to navigate through explorations and adjust filters.
    """
)

st.subheader("Dashboard Preview")
st.info("More interactive visualizations will appear here as you continue building the dashboard.")


# ------------------------------------------------
# Load Data
# ------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_parquet("df_small.parquet")

df = load_data()


# ------------------------------------------------
# Chart 1: Most Popular Start Stations
# ------------------------------------------------
st.header("Most Popular Start Stations")

top_stations = df["start_station_name"].value_counts().head(20).reset_index()
top_stations.columns = ["station", "count"]

fig1 = px.bar(
    top_stations,
    x="station",
    y="count",
    title="Top 20 Most Popular Start Stations",
    labels={"count": "Number of Trips"},
    color="count",
    color_continuous_scale="Viridis"
)

fig1.update_layout(template="plotly_dark", xaxis_tickangle=45)
st.plotly_chart(fig1, use_container_width=True)


# ------------------------------------------------
# Chart 2: Daily Trips vs Temperature
# ------------------------------------------------
st.header("Daily Trips vs. Temperature")

fig2 = px.line(df, x="date", y="trips", title="Daily Trip Volume")
fig2.update_layout(template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)


# ------------------------------------------------
# Folium Map
# ------------------------------------------------
st.header("Trip Flow Map of Top Routes")

with open("NYC_bike_map_with_config.html", "r", encoding="utf-8") as f:
    html_data = f.read()

st.components.v1.html(html_data, height=700, scrolling=True)
