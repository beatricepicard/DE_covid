import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def get_db_conn():
    path = r"..\data\covid_database.db"
    conn = sqlite3.connect(path)
    return conn

def plot_covid_cases_rate(conn, country):
    query = '''
        SELECT cp."Country.Region", 
            cp.Active, 
            cp.Deaths, 
            cp.Recovered, 
            cp.Date,
            wd.Population
        FROM complete cp
        JOIN worldometer_data wd ON cp."Country.Region" = wd."Country.Region"
        WHERE cp."Country.Region" = ?
    '''
    
    # Load the data into a pandas DataFrame
    df = pd.read_sql(query, conn, params=(country,))
    
    # Drop rows with missing values
    df = df.dropna()

    # Check if data is loaded correctly
    if df.empty:
        print(f"No data found for {country}. Please check the country name and data availability.")
        return
    
    # Convert Date column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Calculate rates (percentage of population)
    df['Active_Rate'] = df['Active'] * 100.0 / df['Population']
    df['Deaths_Rate'] = df['Deaths'] * 100.0 / df['Population']
    df['Recovered_Rate'] = df['Recovered'] * 100.0 / df['Population']
    
    # Check if there are any NaN values after calculations
    df = df.dropna(subset=['Active_Rate', 'Deaths_Rate', 'Recovered_Rate'])

    # Calculate the maximum rate for the y-axis
    max_rate = max(df['Active_Rate'].max(), df['Deaths_Rate'].max(), df['Recovered_Rate'].max())

    # Plot the data
    plt.figure(figsize=(8, 5))
    
    # Fill the area under each curve
    plt.fill_between(df['Date'], 0, df['Active_Rate'], color='blue', alpha=0.3, label="Active Cases")
    plt.fill_between(df['Date'], 0, df['Deaths_Rate'], color='red', alpha=0.3, label="Deaths")
    plt.fill_between(df['Date'], 0, df['Recovered_Rate'], color='green', alpha=0.3, label="Recovered")
    
    # Add the year from the Date column to the title
    year = df['Date'].dt.year.iloc[0]  # Get the year from the first row (assuming all dates are from the same year)
    plt.title(f"Covid-19 Case Rates (to population) in {country} ({year})")
    plt.legend(loc='upper left', frameon=False)
    plt.xticks()
    plt.grid()

    # Set x-axis and y-axis limits dynamically
    plt.xlim(pd.Timestamp("2020-01-01"), pd.Timestamp("2020-07-31"))  # January to July 2020
    plt.ylim(0, max_rate * 1.1)  # Adjust y-axis to the max rate with a 10% margin

    # Customize x-axis labels to show dates like 3/1, 4/1, 5/1, etc.
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))  # Default format for month and day

    # Remove leading zeros from the month and day (manual adjustment)
    labels = [label.get_text() for label in plt.gca().get_xticklabels()]
    for i, label in enumerate(labels):
        labels[i] = label.lstrip('0')  # Remove leading zero from the month and day
    plt.gca().set_xticklabels(labels)

    # Customize the x-axis tick locator to display major ticks for each month
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

    # Show plot
    plt.tight_layout()
    plt.show()


def plot_covid_cases_rate_black(conn, country):
    query = '''
        SELECT cp."Country.Region", 
            cp.Active, 
            cp.Deaths, 
            cp.Recovered, 
            cp.Date,
            wd.Population
        FROM complete cp
        JOIN worldometer_data wd ON cp."Country.Region" = wd."Country.Region"
        WHERE cp."Country.Region" = ?
    '''
    
    # Load the data into a pandas DataFrame
    df = pd.read_sql(query, conn, params=(country,))
    
    # Drop rows with missing values
    df = df.dropna()

    # Check if data is loaded correctly
    if df.empty:
        print(f"No data found for {country}. Please check the country name and data availability.")
        return
    
    # Convert Date column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Calculate rates (percentage of population)
    df['Active_Rate'] = df['Active'] * 100.0 / df['Population']
    df['Deaths_Rate'] = df['Deaths'] * 100.0 / df['Population']
    df['Recovered_Rate'] = df['Recovered'] * 100.0 / df['Population']
    
    # Check if there are any NaN values after calculations
    df = df.dropna(subset=['Active_Rate', 'Deaths_Rate', 'Recovered_Rate'])

    # Calculate the maximum rate for the y-axis
    max_rate = max(df['Active_Rate'].max(), df['Deaths_Rate'].max(), df['Recovered_Rate'].max())

    # Plot the data
    plt.figure(figsize=(8, 5))
    
    # Set the background color to black
    plt.gcf().set_facecolor('dimgray')  # Set figure background to black
    plt.gca().set_facecolor('dimgray')  # Set axis background to black
    
    # Fill the area under each curve (shading)
    plt.fill_between(df['Date'], 0, df['Active_Rate'], color='blue', alpha=0.3, label="Active Cases")
    plt.fill_between(df['Date'], 0, df['Deaths_Rate'], color='red', alpha=0.3, label="Deaths")
    plt.fill_between(df['Date'], 0, df['Recovered_Rate'], color='green', alpha=0.3, label="Recovered")
    
    # Formatting
    plt.xlabel("Date", color='white')  # Set x-axis label color to white
    plt.ylabel("Percentage of Population", color='white')  # Set y-axis label color to white
    plt.title(f"Covid-19 Case Rates in {country} ({df['Date'].dt.year.iloc[0]})", color='white')  # Set title color to white
    
    # Move legend to top-left
    plt.legend(loc='upper left', frameon=False, facecolor='dimgrey', edgecolor='white', fontsize=10, labelcolor='white')  # Legend in white

    plt.xticks(color='white')  # Set x-axis tick color to white
    plt.yticks(color='white')  # Set y-axis tick color to white
    plt.grid(color='white', linestyle='--', linewidth=0.5)  # Set grid color to white

    # Set x-axis and y-axis limits dynamically
    plt.xlim(pd.Timestamp("2020-01-01"), pd.Timestamp("2020-07-31"))  # January to July 2020
    plt.ylim(0, max_rate * 1.1)  # Adjust y-axis to the max rate with a 10% margin

    # Customize x-axis labels to show dates like 3/1, 4/1, 5/1, etc.
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))  # Default format for month and day

    # Remove leading zeros from the month and day (manual adjustment)
    labels = [label.get_text() for label in plt.gca().get_xticklabels()]
    for i, label in enumerate(labels):
        labels[i] = label.lstrip('0')  # Remove leading zero from the month and day
    plt.gca().set_xticklabels(labels)

    # Customize the x-axis tick locator to display major ticks for each month
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

    # Show plot
    plt.tight_layout()
    plt.show()

db_conn = get_db_conn()  
plot_covid_cases_rate(db_conn, "Germany")
plot_covid_cases_rate_black(db_conn, "China")
db_conn.close()