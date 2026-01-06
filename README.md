# NYC CitiBike Analysis (2022) 🚲🗽

This project analyzes **NYC CitiBike trip patterns in 2022** and combines them with **NOAA daily weather data** (Central Park station) to understand how ridership changes over time, across seasons, and around high-demand stations. The results are presented in an interactive **Streamlit dashboard** designed to support decisions related to **bike supply and rebalancing**.

## Live Dashboard
Streamlit App: https://ny-citybike-analysis-mjac8jcdq8xcs2qg3tbyxl.streamlit.app

---

## Project Goals
- Clean and prepare CitiBike 2022 trip data
- Retrieve and merge daily weather summaries from NOAA
- Explore ridership trends, seasonality, and station demand
- Visualize findings in a Streamlit dashboard with charts and an interactive map
- Extract insights relevant to NYC CitiBike’s **supply imbalance problem** (empty/full stations)

---

## Research Questions

### Ridership Trends
- Which months have the highest and lowest number of trips?
- How do weekday vs weekend patterns differ?
- What are the major demand peaks?

### Weather Relationship
- Does temperature influence ridership volume?
- How do adverse conditions (rain/snow) affect activity?

### Station Analysis
- What are the most popular start stations?
- Where are demand hotspots geographically?
- Which areas are most likely to experience supply pressure?

### Trip Characteristics
- What does typical trip behavior look like (duration, usage patterns)?
- How do member vs casual riders differ? *(if available in data sample)*

---

## Dashboard Pages (Streamlit)
The dashboard is organized into pages using `st.sidebar.selectbox`:

1. **Intro**
   - Summary and key context for the project

2. **Daily Trips vs Temperature**
   - Dual-axis time series linking demand and weather
   - Markdown interpretation of the relationship and implications for forecasting

3. **Most Popular Stations**
   - Bar chart of top start stations by total trips
   - Interpretation highlighting demand concentration and supply impact

4. **Interactive Map**
   - Embedded HTML map export (Folium)
   - Interpretation describing spatial hotspots / route patterns

5. **Extra Insight (Seasonality)**
   - Seasonal demand vs average temperature view
   - Interpretation focused on operational planning

6. **Recommendations**
   - Actionable suggestions for rebalancing strategy and forecasting

---

## Data Sources

### CitiBike Trips
- CitiBike trip data (2022)

### Weather (NOAA)
Weather data retrieved from **NOAA Climate Data Online (CDO)**  
Dataset: **GHCND – Daily Summaries**  
Station: **USW00094728 (NYC Central Park)**

---

## Repo Structure 
- `CitiBike_Dashboard.py` – Streamlit dashboard script
- `citibike_sample_1.parquet` – reduced dataset used for dashboard performance
- `*.html` – exported interactive maps (embedded in Streamlit)
- Notebooks (`2.x_*.ipynb`)

