import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px
from aggregation import aggregation
from country_summary import country_summary
from get_countries import get_countries


#connection to DB
db_path = "../data/covid_database.db"
connection = sqlite3.connect(db_path)
df = pd.read_sql("SELECT * FROM complete", connection)
df_country, df_county, df_continent = aggregation(df, connection)

#date conversion & finding date range
df["Date"] = pd.to_datetime(df["Date"])
min_date = df["Date"].min()
max_date = df["Date"].max()

#sorting countries
df_country = df_country.sort_values(by="Country.Region")
countries = df_country["Country.Region"].unique().tolist()


#starting dashboard
st.set_page_config(page_title="COVID-19 Professional Dashboard", layout="wide")
st.title("COVID-19 Dashboard")

#sidebar
st.sidebar.header("Filter Options")
selected_country = st.sidebar.selectbox("Select Country:", countries, index=countries.index("Netherlands")) #setting Netherlands as starting country
date_range = st.sidebar.date_input("Select Date Range:", [min_date, max_date], min_value=min_date, max_value=max_date)
start_date, end_date = pd.to_datetime(date_range)

if start_date > end_date:
    st.sidebar.error("End date must be after start date!")

#filtering data based on selected date range and selected country
df_filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
df_country_filtered = df_filtered[df_filtered["Country.Region"] == selected_country]


#worldwide numeric values on dashboard
st.markdown("###Global COVID-19 Statistics") #hashtags makes text appeare smaller
col1, col2, col3, col4 = st.columns(4) #creates 4 colums
col1.metric("Confirmed", f"{df_filtered['Confirmed'].sum():,}")
col2.metric("Recovered", f"{df_filtered['Recovered'].sum():,}")
col3.metric("Deaths", f"{df_filtered['Deaths'].sum():,}")
col4.metric("Active", f"{df_filtered['Active'].sum():,}")

#graphs for COVID-19 trends and global spread
st.markdown("### COVID-19 Trends & Global Spread")
col1, col2, col3, col4 = st.columns(4)

with col1:
    fig_confirmed = px.bar(df_filtered, x="Date", y="Confirmed", title="Confirmed Cases Over Time", color_discrete_sequence=["blue"])
    st.plotly_chart(fig_confirmed, use_container_width=True)
    fig_map_confirmed = px.scatter_geo(df_country, locations="Country.Region", locationmode="country names", size="Confirmed", title="Confirmed Cases Worldwide", color_discrete_sequence=["blue"])
    st.plotly_chart(fig_map_confirmed, use_container_width=True)
    #fig_bar_confirmed = px.bar(df_continent, x ="Confirmed", y = "Continent", orientation = 'h', title = "Total Confirmed Cases by Continent", color = "Confirmed", color_continuous_scale = "Blues") 
    #st.plotly_chart(fig_bar_confirmed, use_container_width=True)

with col2:
    fig_recovered = px.bar(df_filtered, x="Date", y="Recovered", title="Recovered Cases Over Time", color_discrete_sequence=["green"])
    st.plotly_chart(fig_recovered, use_container_width=True)
    fig_map_recovered = px.scatter_geo(df_country, locations="Country.Region", locationmode="country names", size="Recovered", title="Recovered Cases Worldwide", color_discrete_sequence=["green"])
    st.plotly_chart(fig_map_recovered, use_container_width=True)

with col3:
    fig_deaths = px.bar(df_filtered, x="Date", y="Deaths", title="Deaths Over Time", color_discrete_sequence=["purple"])
    st.plotly_chart(fig_deaths, use_container_width=True)
    fig_map_deaths = px.scatter_geo(df_country, locations="Country.Region", locationmode="country names", size="Deaths", title="Deaths Worldwide", color_discrete_sequence=["purple"])
    st.plotly_chart(fig_map_deaths, use_container_width=True)

with col4:
    fig_active = px.bar(df_filtered, x="Date", y="Active", title="Active Cases Over Time", color_discrete_sequence=["orange"])
    st.plotly_chart(fig_active, use_container_width=True)
    fig_map_active = px.scatter_geo(df_country, locations="Country.Region", locationmode="country names", size="Active", title="Active Cases Worldwide", color_discrete_sequence=["orange"])
    st.plotly_chart(fig_map_active, use_container_width=True)



# --- COUNTRY COMPARISON ---
st.markdown("### Top 10 Affected Countries")
df_top_countries = df_country.sort_values(by="Confirmed", ascending=False).head(10)
top_countries_fig = px.bar(df_top_countries, x="Confirmed", y="Country.Region", title="Top 10 Countries by Confirmed Cases", color="Confirmed", orientation='h')
st.plotly_chart(top_countries_fig, use_container_width=True)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    body, .stApp {
        background-color: #D3D3D3; /* Helles Grau für den Hauptbereich */
        color: #000000; /* Schwarzer Text */
        font-family: 'Montserrat', sans-serif; /* Neue Schriftart */
    }

    .stSidebar {
    background-color: #777777; /* Mittelgrau für die Sidebar */
    color: #FFFFFF;
    font-family: 'Montserrat', sans-serif;
    }

    .stSelectbox, .stDateInput, .stMetric, .stPlotlyChart {
        background-color: #F0F0F0; /* Noch helleres Grau für Elemente */
        color: #000000;
        border-radius: 10px;
        padding: 8px;
        font-family: 'Montserrat', sans-serif;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 700; /* Dickere Überschriften */
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --- DATABASE CONNECTION CLOSE ---
connection.close()
