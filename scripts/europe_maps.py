import sqlite3
import pandas as pd
import plotly.express as px

# A function that prints a map of Europe, showing the active cases per person in the different countries.
def maps(connection): 
    query = f"SELECT \"Country.Region\", ActiveCases, Population FROM worldometer_data WHERE Continent == 'Europe'"
    df = pd.read_sql(query, connection)
    df["ActiveCases/Pop."] = df["ActiveCases"] / df["Population"]

    fig = px.choropleth(df, scope="europe", color="ActiveCases/Pop.",
    color_continuous_scale="rdylgn_r",
    locations="Country.Region",
    locationmode="country names",
    title="European Countries with Active Cases")
    fig.show()
    
    connection.close()
    return
