# NY-CitiBike-Analysis


This project explores CitiBike trip data from 2022 and merges it with NOAA weather data to analyze ridership patterns, seasonal effects, station usage, and trip behaviors across New York City.

The goal is to prepare and visualize insights in an interactive dashboard that helps answer key transportation and urban planning questions.

---

##  Project Overview
This project focuses on:
- Cleaning and processing the CitiBike 2022 dataset  
- Collecting daily weather summaries from NOAA  
- Joining ridership with temperature & precipitation  
- Answering analytical questions  
- Creating a dashboard visualization plan  

It serves as the foundation for a full interactive dashboard.

---

##  Research Questions

### **Ridership Trends**
- Which months have the highest and lowest number of trips?  
- How do weekend vs weekday patterns differ?  
- What are the hourly ridership peaks?

### **Weather Relationship**
- Does temperature influence ridership volume?  
- How do rainy or snowy days affect biking activity?

### **Station Analysis**
- What are the most popular start and end stations?  
- Which station-to-station trips are most common?  
- Are stations evenly distributed geographically?

### **Trip Characteristics**
- What is the typical ride duration?  
- How do members vs casual riders behave differently?

---

##  Planned Dashboard Components

### **1. Key Metrics**
- Total rides  
- Average trip duration  
- Member vs casual distribution  
- Hottest/coldest days with trip counts  

### **2. Trends and Usage Patterns**
- Monthly ridership (line chart)  
- Day-of-week usage (bar chart)  
- Hour-of-day patterns (heatmap)  

### **3. Weather & Ridership**
- Temperature vs trips (scatterplot + trendline)  
- Rides on rainy vs dry days (bar/line chart)

### **4. Station Analysis**
- Most popular stations (bar chart)  
- Most common OD pairs (flow/Sankey)  
- Map showing station distribution

### **5. Trip Duration**
- Histogram or boxplot of trip lengths  
---

## 🌦️ Weather Data Source
Weather data is retrieved from:

**NOAA Climate Data Online (CDO)**  
Dataset: **GHCND – Daily Summaries**  
Station: **USW00094728 (NYC Central Park)**  

---

## 🛠️ Technologies Used
- Python 3.9+
- Pandas
- NumPy
- Matplotlib / Seaborn / Plotly
- Requests (NOAA API)
- Folium / Geopandas (mapping)
- Jupyter Notebooks

---
