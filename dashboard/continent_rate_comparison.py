import pandas as pd

def get_continent_rates(conn, start_date, end_date):

    start_date = start_date.strftime('%m/%d/%Y')
    end_date = end_date.strftime('%m/%d/%Y')

    # Base SQL query
    query = """
        SELECT Date, Continent, 
            CAST(ROUND(ConfirmedPerPop, 0) AS INTEGER) AS ConfirmedPerPop,
            CAST(ROUND(DeathPerPop, 0) AS INTEGER) AS DeathPerPop,
            CAST(ROUND(RecoveredPerPop, 0) AS INTEGER) AS RecoveredPerPop
        FROM continents_rates
        WHERE Date BETWEEN ? AND ?
        """
    # Execute SQL query
    df = pd.read_sql_query(query, conn, params=(start_date, end_date))

    df_start = df[df["Date"] == str(start_date)]
    df_end = df[df["Date"] == str(end_date)]

    # Merge the dataframes for start and end date to compute rate differences
    df_merged = pd.merge(df_end, df_start, on="Continent", suffixes=("_end", "_start"))

    # Calculate rate differences
    df_merged["ConfirmedPerPop_diff"] = df_merged["ConfirmedPerPop_end"] - df_merged["ConfirmedPerPop_start"]
    df_merged["DeathPerPop_diff"] = df_merged["DeathPerPop_end"] - df_merged["DeathPerPop_start"]
    df_merged["RecoveredPerPop_diff"] = df_merged["RecoveredPerPop_end"] - df_merged["RecoveredPerPop_start"]
 
    df_sorted = df_merged.sort_values(by="ConfirmedPerPop_diff", ascending=True)

    return df_sorted