import sqlite3
import pandas as pd


def country_summary(country_name, connection):
    query = f"""
    SELECT cw."Country.Region",
           SUM(cw.Confirmed) AS total_cases,
           SUM(cw.Deaths) AS total_deaths,
           SUM(cw.Recovered) AS total_recovered,
           SUM(cw.Active) AS total_active,
           wd.Population
    FROM country_wise cw
    LEFT JOIN worldometer_data wd
    ON cw."Country.Region" = wd."Country.Region"
    WHERE cw."Country.Region" = ?
    GROUP BY cw."Country.Region";
    """

    df = pd.read_sql(query, connection, params=[country_name])
    result = {
        "Country": df.iloc[0]["Country.Region"],
        "Total Confirmed Cases": int(df.iloc[0]["total_cases"]),
        "Total Deaths": int(df.iloc[0]["total_deaths"]),
        "Total Recovered Cases": int(df.iloc[0]["total_recovered"]),
        "Total Active Cases": int(df.iloc[0]["total_active"]),
        "Population": int(df.iloc[0]["Population"]) if pd.notna(df.iloc[0]["Population"]) else "Unknown" }
    
    return result