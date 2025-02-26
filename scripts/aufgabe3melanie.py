##Compare the estimated death rate (μ) over the different continents. Visualize this in a barplot
#table worldometer_data -> 'continent' -> death_rate = ∆D(t)/I(t) -> Sum of 'TotalDeaths' / 'TotalCases'
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


#Creates Pandas DataFrame
def data(query, path):
    conn = sqlite3.connect(path)
    df = pd.read_sql(query, conn)
    conn.close()
    return df

#Task 3.5.1 - Death rate by continent
def death_rate_by_continent(path):
    query = '''
        SELECT Continent, 
            COALESCE(SUM(TotalDeaths), 0) AS total_deaths, 
            COALESCE(SUM(TotalCases), 0) AS total_cases
        FROM worldometer_data
        WHERE Continent IS NOT NULL AND TRIM(Continent) != ''
        GROUP BY Continent;
    '''
    df = data(query, path)
    if 'total_deaths' in df.columns and 'total_cases' in df.columns:
        df['death_rate'] = df['total_deaths'] / df['total_cases']
        df['death_rate'].replace([float('inf'), float('-inf')], 0, inplace=True)
        df['death_rate'].fillna(0, inplace=True)
    else:
        df['death_rate'] = 0
    
    return df

#Task 3.5.2 - Plot death rate by continent
def plot_death_rate(df):
    plt.figure(figsize=(10,5))
    colors = plt.cm.viridis(np.linspace(0, 1, len(df)))
    plt.bar(df['Continent'], df['death_rate'], color=colors)
    plt.xlabel('Continent')
    plt.ylabel('Estimated Death Rate')
    plt.title('Estimated Death Rate by Continent')
    plt.xticks(rotation=45)
    plt.show()


#Task 3.6 - Top 5 US counties with most deaths and most reccorded cases
def top_us_counties(path):
    query = '''
        SELECT Admin2 AS County, Province_State AS State, 
               COALESCE(SUM(Deaths), 0) AS total_deaths, 
               COALESCE(SUM(Confirmed), 0) AS total_cases
        FROM usa_county_wise
        WHERE Country_Region = 'US'
        GROUP BY County, State
    '''
    df = data(query, path)
    top5_deaths = df.nlargest(5, 'total_deaths')
    top5_cases = df.nlargest(5, 'total_cases')
    
    return top5_deaths, top5_cases




