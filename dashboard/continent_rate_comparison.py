import pandas as pd

def get_continent_rates(conn, start_date, end_date):

    # Convert start_date and end_date to MM/DD/YYYY string format for sql query
    start_date = start_date.strftime('%m/%d/%Y')
    end_date = end_date.strftime('%m/%d/%Y')
    
    # Query to get data from Cases_rates table for the selected Date Range
    query = """
    SELECT Date, Continent, Confirmed_rate, Death_rate
    FROM continents_rates
    WHERE Date BETWEEN ? AND ?
    """

    df = pd.read_sql_query(query, conn, params=(start_date, end_date))

    df_start = df[df["Date"] == str(start_date)]
    df_end = df[df["Date"] == str(end_date)]

    # Merge the dataframes for start and end date to compute rate differences for Confirmed, Deaths
    df_merged = pd.merge(df_end, df_start, on="Continent", suffixes=("_end", "_start"))

    # Calculate rate differences
    df_merged["Confirmed_rate_diff"] = df_merged["Confirmed_rate_end"] - df_merged["Confirmed_rate_start"]
    df_merged["Death_rate_diff"] = df_merged["Death_rate_end"] - df_merged["Death_rate_start"]
 
    df_sorted = df_merged.sort_values(by="Confirmed_rate_diff", ascending=True)

    return df_sorted