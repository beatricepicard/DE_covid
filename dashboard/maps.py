import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from datetime import datetime

# removes problematic countries that show false data
def remove_countries(df):
    countries = ["Sweden"]
    df_clean = df[~df["Country"].isin(countries)]
    return df_clean

# A function that generates a map of the chosen continent, showing the percentage of active cases in the population.
def continent_map(connection, continent, date):
    query_continent = f"SELECT * FROM new_complete WHERE Continent = '{continent}' AND Date = '{date}'" 
    df = pd.read_sql(query_continent, connection)
    df = remove_countries(df)
    df = df[df["ActivePerPop"].notna() & (df["ActivePerPop"] >= 0)]
    lower_continent = continent.lower()
    max_value = min(df["ActivePerPop"].max(), 0.0035)

    fig = px.choropleth(df, scope=lower_continent, color="ActivePerPop",
                        color_continuous_scale= 'ylgnbu', locations="Country",
                        locationmode="country names", title= f"Active Cases in {continent} on {date}",
                        hover_name = "Country", range_color=[0, max_value])
    fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Active Cases: %{z:.5%}")
    fig.update_layout(coloraxis_colorbar=dict(title="Active Cases (%)", tickformat=".2%"), dragmode=False,  autosize=True, margin=dict(t=25, b=0, l=30, r=30))
    st.plotly_chart(fig, use_container_width=True)
    if continent == "Europe":
        st.markdown("**Note:** Sweden has been left out, because the data appears to be inaccurate/incomplete.")
    return

# A function that generates a world map, showing the percentage of active cases in the population.
def world_map(connection, date):
    query_world = f"SELECT * FROM new_complete WHERE Date = '{date}'" 
    df = pd.read_sql(query_world, connection)
    df = remove_countries(df)

    max_value = min(df["ActivePerPop"].max(), 0.0035)

    fig = px.choropleth(df, scope="world", color="ActivePerPop",
                        color_continuous_scale= 'ylgnbu', locations="Country",
                        locationmode="country names", title= f"Active Cases on {date}",
                        hover_name = "Country", range_color=[0, max_value])
    fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Active Cases: %{z:.5%}")
    fig.update_layout(coloraxis_colorbar=dict(title="Active Cases (%)", tickformat=".2%"), dragmode=False, autosize=True, margin=dict(t=25, b=0, l=30, r=30), height = 400)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("**Note:** Some countries might have been left out, because the data appears to be inaccurate/incomplete.")
    return

