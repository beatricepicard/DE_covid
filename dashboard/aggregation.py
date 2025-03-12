
import pandas as pd
import sqlite3


def aggregation(cleaned_df, connection):
    worldometer_df = pd.read_sql("SELECT * FROM worldometer_data", connection)

    #Country Aggregation
    df_country = cleaned_df.groupby("Country.Region").agg({
        "Confirmed": "sum",
        "Deaths": "sum",
        "Recovered": "sum",
        "Active": "sum"
    }).reset_index()

    # Add population from worldometer dataset
    population_df = worldometer_df[["Country.Region", "Population"]]
    df_country = df_country.merge(population_df, on="Country.Region", how="left")

    #County Aggregation
    df_county = cleaned_df.groupby(["Province.State", "Country.Region"]).agg({
        "Confirmed": "sum",
        "Deaths": "sum",
        "Recovered": "sum",
        "Active": "sum"
    }).reset_index()

    #Continent Aggregation
    df_continent = worldometer_df.groupby("Continent").agg({
        "TotalCases": "sum",
        "TotalDeaths": "sum",
        "TotalRecovered": "sum",
        "ActiveCases": "sum",
        "Population": "sum"
    }).reset_index()


    return df_country, df_county, df_continent