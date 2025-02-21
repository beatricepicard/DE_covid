import sqlite3
import pandas as pd

path = r"..\data\covid_database.db"
conn = sqlite3.connect(path)
cursor = conn.cursor()

query_country = f"""
SELECT "Country.Region", Confirmed, Deaths, Recovered, Active, "New.cases", "New.deaths", "New.recovered"
FROM country_wise
"""

query_population = f"""
SELECT "Country.Region", Population
FROM worldometer_data
"""

df_country = pd.read_sql(query_country, conn)
df_population = pd.read_sql(query_population, conn)

conn.close()

df_merged = pd.merge(df_country, df_population, on="Country.Region", how="left")

df_merged["Susceptible"] = (df_merged["Population"] - df_merged["Active"] - df_merged["Deaths"] - df_merged["Recovered"])
df_merged["mu"] = df_merged["New.deaths"]/df_merged["Active"]
df_merged["gamma"] = 1/4.5
df_merged["beta"] = (df_merged["New.cases"] + (df_merged["mu"] + df_merged["gamma"]) * df_merged["Active"])/ (df_merged["Susceptible"] *(df_merged["Active"]/ df_merged["Population"] ))
df_merged["alpha"] = (df_merged["gamma"] * df_merged["Active"] - df_merged["New.recovered"])/ df_merged["Recovered"]


def parameters_for_country(country, dataframe):
    country_data = dataframe[dataframe["Country.Region"] == country]

    if country_data.empty:
        print(f"No data available for {country}.")
        return None
    
    alpha = country_data["alpha"].values[0]
    beta = country_data["beta"].values[0]
    gamma = country_data["gamma"].values[0]
    mu = country_data["mu"].values[0]

    print(f"The parameters for {country} are given by: alpha = {alpha:.3f}, beta = {beta:.3f}, gamma = {gamma:.3f}, mu = {mu:.3f}")

parameters_for_country("Greece", df_merged)

