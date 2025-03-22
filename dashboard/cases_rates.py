import pandas as pd

'''The function is used for creating a visualisation 
"Countries comparison including selected country" on the "COVID-19 Dashboard" by:
- Retrieving data from covid_database table "new_complete" for different countries.
- Filtering data by continent if a specific one is selected.
- Converting case rates by population to cases per million people for better readability.
- Calculating changes in cases metrics between a specified start and end date. 
- Sorting the results based on confirmed case rate differences.
- Providing a structured dataset for further visualization'''

def get_cases_rates(conn, start_date, end_date, continent):

    # Base SQL query
    query = """
        SELECT Date, Country, 
            CAST(ROUND(ConfirmedPerPop * 1000000, 0) AS INTEGER) AS ConfirmedPerPop, 
            CAST(ROUND(DeathsPerPop * 1000000, 0) AS INTEGER) AS DeathsPerPop, 
            CAST(ROUND(RecoveredPerPop * 1000000, 0) AS INTEGER) AS RecoveredPerPop
        FROM new_complete
        WHERE Date BETWEEN ? AND ?
        """
    params = [start_date, end_date]

    # Add continent filter if not "All"
    if continent != "All":
        query += " AND Continent = ?"
        params += [continent]

    # Execute SQL query
    df = pd.read_sql_query(query, conn, params=(params))

    df_start = df[df["Date"] == str(start_date)]
    df_end = df[df["Date"] == str(end_date)]

    # Merge the two DataFrames on "Country" so that columns get suffixes _start and _end
    df_merged = pd.merge(df_end, df_start, on="Country", suffixes=("_end", "_start"))

    # Compute rate differences
    df_merged["ConfirmedPerPop_diff"] = df_merged["ConfirmedPerPop_end"] - df_merged["ConfirmedPerPop_start"]
    df_merged["DeathsPerPop_diff"] = df_merged["DeathsPerPop_end"] - df_merged["DeathsPerPop_start"]
    df_merged["RecoveredPerPop_diff"] = df_merged["RecoveredPerPop_end"] - df_merged["RecoveredPerPop_start"]

    # Sort by confirmed cases per population difference
    df_sorted = df_merged.sort_values(by="ConfirmedPerPop_diff", ascending=False)

    return df_sorted