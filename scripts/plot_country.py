import pandas as pd
import matplotlib.pyplot as plt
import sqlite3 


def plot_country_statistics(country_name, connection):
    """
    Generates graphical summaries for a selected country, including:
    - Confirmed cases, deaths, recoveries, active cases over time
    - SIR Model projection (if applicable)
    """
    query = f"""
    SELECT Date, Confirmed, Deaths, Recovered, Active
    FROM complete
    WHERE "Country.Region" = ?
    ORDER BY Date;
    """
    
    df = pd.read_sql(query, connection, params=[country_name])
    
    if df.empty:
        print(f"No data found for {country_name}.")
        return
    
    df["Date"] = pd.to_datetime(df["Date"])

    # Plot COVID-19 trends
    plt.figure(figsize=(12, 6))
    plt.plot(df["Date"], df["Confirmed"], label="Confirmed Cases", color="blue")
    plt.plot(df["Date"], df["Deaths"], label="Deaths", color="red")
    plt.plot(df["Date"], df["Recovered"], label="Recovered", color="green")
    plt.plot(df["Date"], df["Active"], label="Active Cases", color="orange")

    plt.xlabel("Date")
    plt.ylabel("Number of Cases")
    plt.title(f"COVID-19 Trends in {country_name}")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

    print(f"Graphical summary for {country_name} displayed.")

