import pandas as pd
import sqlite3 as sql

def group_by_country(connection):
    query_1 = f"SELECT * FROM complete"
    df = pd.read_sql(query_1, connection)
    print(df)

    grouped_by_country = df.groupby('Country.Region').agg({
        'Confirmed': 'sum',
        'Deaths': 'sum',
        'Recovered': 'sum',
        'Active': 'sum'
    }).reset_index()
    print(grouped_by_country)

    return grouped_by_country


def group_by_state(connection):
    query_2 = f"SELECT * FROM usa_county_wise"
    df = pd.read_sql(query_2, connection)
    print(df)

    grouped_by_state = df.groupby('Province_State'). agg({
        'Confirmed': 'sum',
        'Deaths': 'sum'
    }).reset_index()
    print(grouped_by_state)

    return grouped_by_state
