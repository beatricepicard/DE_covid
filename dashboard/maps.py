import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# A function that looks for missing values in worldometer.csv and fills them up with values from country_wise.csv
def complete_data(df_worldometer, df_country):
    df_country = df_country.copy()
    df_country.set_index('Country.Region', inplace=True)
    df_worldometer.set_index('Country.Region', inplace=True)
    df_worldometer['ActiveCases'] = df_worldometer['ActiveCases'].combine_first(df_country['Active'])
    df_worldometer.reset_index(inplace=True)
    return df_worldometer

# Manually adding continent name and population in 2020 for countries which are not in the worldometer file of the database.
def add_missing_countries(df_worldometer, df_country):
    country_wise_set = set(df_country['Country.Region'])
    worldometer_set = set(df_worldometer['Country.Region'])
    missing_countries = country_wise_set - worldometer_set
    missing_data = df_country[df_country['Country.Region'].isin(missing_countries)]

    continent_mapping = {
    'Brunei': 'Asia',
    'Kosovo': 'Europe',
    'China': 'Asia',
    'United Kingdom': 'Europe'
    }

    population_mapping = {
    'Brunei': 440000,
    'China': 1.41e+09,
    'Kosovo': 1800000,
    'United Kingdom': 68000000
    }

    exclude_countries = ['Central African Republic', 'South Korea', 'US']
    missing_data = missing_data[~missing_data['Country.Region'].isin(exclude_countries)]
    missing_data_df = pd.DataFrame(columns=df_worldometer.columns)
    missing_data_df["Country.Region"] = missing_data["Country.Region"]
    missing_data_df["ActiveCases"] = missing_data["Active"]
    missing_data_df["Continent"] = missing_data_df["Country.Region"].map(continent_mapping)
    missing_data_df["Population"] = missing_data_df["Country.Region"].map(population_mapping)
    missing_data_df.fillna(np.nan, inplace=True)

    df_worldometer = pd.concat([df_worldometer, missing_data_df], ignore_index=True)
    return df_worldometer

# Retrieving the data from the database and calling the functions that complete and clean it.
def get_data(connection):
    query_worldometer = f"SELECT * FROM worldometer_data"
    df_worldometer = pd.read_sql(query_worldometer, connection)

    query_country = f"SELECT \"Country.Region\", Active FROM country_wise"
    df_country = pd.read_sql(query_country, connection)

    df_worldometer = complete_data(df_worldometer, df_country)
    df_worldometer = add_missing_countries(df_worldometer, df_country)

    df_worldometer["Country.Region"] = df_worldometer["Country.Region"].replace({
        'CAR': 'Central African Republic'})
    return df_worldometer


# A function that generates a map of the chosen continent, showing the percentage of active cases in the population.
def continent_map(connection, continent):
    df_worldometer = get_data(connection)
    df = df_worldometer[df_worldometer["Continent"] == continent].copy()
    df["ActiveCases/Pop."] = df["ActiveCases"] / df["Population"]

    lower_continent = continent.lower()
    fig = px.choropleth(df, scope=lower_continent, color="ActiveCases/Pop.",
    color_continuous_scale="rdylgn_r",
    locations="Country.Region",
    locationmode="country names",
    title= f"Active Cases in {continent}",
    hover_name = "Country.Region")
    fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Active Cases: %{z:.4%}")
    fig.update_layout(coloraxis_colorbar=dict(title="Active Cases (%)", tickformat=".1%"))
    st.plotly_chart(fig)
    return

# A function that generates a world map, showing the percentage of active cases in the population.
def world_map(connection):
    df_worldometer = get_data(connection)
    df_worldometer["ActiveCases/Pop."] = df_worldometer["ActiveCases"] / df_worldometer["Population"]

    fig = px.choropleth(df_worldometer, scope="world", color="ActiveCases/Pop.",
    color_continuous_scale="rdylgn_r",
    locations="Country.Region",
    locationmode="country names",
    title= f"Active Cases in the whole world",
    hover_name = "Country.Region")
    fig.update_traces(hovertemplate="<b>%{hovertext}</b><br>Active Cases: %{z:.4%}")
    fig.update_layout(coloraxis_colorbar=dict(title="Active Cases (%)", tickformat=".1%"))
    st.plotly_chart(fig)
    return