import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
import datetime

# Manually filling in continents that are missing
def fill_in_continents(df):
    continent_dict = {
        "Brunei": "Asia",
        "Central African Republic": "Africa",
        "China": "Asia",
        "United Kingdom": "Europe",
        "Burma": "Asia",
        "Kosovo": "Europe",
        "South Korea": "Asia",
        "United Arab Emirates": "Asia",
        "Congo (Brazzaville)": "Africa",
        "Congo (Kinshasa)": "Africa",
        "Cote d'Ivoire": "Africa",
        "US": "North America",
    }
    df['Continent'] = df['Continent'].fillna(df['Country'].map(continent_dict))
    return df

# Function that adds the continents to the complete dataframe
def add_continents(df, connection):
    query = f"SELECT \"Country.Region\", Continent FROM worldometer_data"
    df_continents =  pd.read_sql(query, connection)
    df_continents_clean = df_continents.dropna(subset=['Continent'])
    merged_continents = pd.merge(df, df_continents_clean, left_on="Country", right_on="Country.Region", how="left")
    return merged_continents

# Function that adds up values for countries with several territories, such as France or the UK
def aggregate_territories(df):
    df_aggregated = df.groupby('Country').agg({
        'Active': 'sum',
        'Population': 'first'
    }).reset_index()
    return df_aggregated

# removes problematic countries that show false data
def remove_countries(df):
    countries = ["Sweden", "Papua New Guinea"]
    df_clean = df[~df["Country"].isin(countries)]
    return df_clean

# A function that generates a map of the chosen continent, showing the percentage of active cases in the population.
def continent_map(df, continent, date, connection):
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df = remove_countries(df)
    df_complete = add_continents(df, connection)
    df_complete_filled = fill_in_continents(df_complete)
    df_continent = df_complete[(df_complete["Continent"] == continent) & (df_complete["Date"] == date)].copy()
    df_continent = df_continent[~df_continent.duplicated(subset=["Country", "Date"], keep="first")]
    agg_df_continent = aggregate_territories(df_continent)
    agg_df_continent["ActiveCases/Pop."] = agg_df_continent["Active"] / agg_df_continent["Population"]
    agg_df_continent = agg_df_continent.drop_duplicates()

    lower_continent = continent.lower()
    max_value = min(agg_df_continent["ActiveCases/Pop."].max(), 0.005)
    fig = px.choropleth(agg_df_continent, scope=lower_continent, color="ActiveCases/Pop.",
                        color_continuous_scale="rdylgn_r", locations="Country",
                        locationmode="country names", title= f"Active Cases in {continent}",
                        hover_name = "Country", range_color=[0, max_value])
    fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Active Cases: %{z:.5%}")
    fig.update_layout(coloraxis_colorbar=dict(title="Active Cases (%)", tickformat=".1%"))
    st.plotly_chart(fig)
    return

# A function that generates a world map, showing the percentage of active cases in the population.
def world_map(df, date):
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df_world = df[df["Date"] == date]
    df_world = remove_countries(df_world)
    df_world = df_world[~df_world.duplicated(subset=["Country", "Date"], keep="first")]
    agg_df_world = aggregate_territories(df_world)
    agg_df_world["ActiveCases/Pop."] = agg_df_world["Active"] / agg_df_world["Population"]

    max_value = min(agg_df_world["ActiveCases/Pop."].max(), 0.005)
    fig = px.choropleth(agg_df_world, scope="world", color="ActiveCases/Pop.",
                        color_continuous_scale="rdylgn_r", locations="Country",
                        locationmode="country names", title= f"Active Cases in the whole world",
                        hover_name = "Country", range_color=[0, max_value])
    fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Active Cases: %{z:.5%}")
    fig.update_layout(coloraxis_colorbar=dict(title="Active Cases (%)", tickformat=".1%"))
    st.plotly_chart(fig)
    return