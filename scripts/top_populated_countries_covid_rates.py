import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_db_conn():
    path = r"..\data\covid_database.db"
    conn = sqlite3.connect(path)
    return conn

def plot_covid_cases_rate(conn):
    query = '''
        SELECT "Country.Region", 
            ActiveCases, 
            TotalDeaths, 
            TotalRecovered, 
            Population
        FROM worldometer_data
        ORDER BY Population DESC
        LIMIT 20
    '''
    # Load the data into a pandas DataFrame
    df = pd.read_sql(query, conn)
    df = df.dropna()
    
    # Calculate rates
    df['Active_Rate'] = df['ActiveCases']*100.0 / df['Population']
    df['Deaths_Rate'] = df['TotalDeaths']*100.0 / df['Population']
    df['Recovered_Rate'] = df['TotalRecovered']*100.0 / df['Population']
    
    # Create a total rate column and sort in descending order
    df['Total_Rate'] = df['Active_Rate'] + df['Deaths_Rate'] + df['Recovered_Rate']
    df = df.sort_values(by='Total_Rate', ascending=False)  

    # Determine x-axis range
    max_percentage = df['Total_Rate'].max()

    # Plot the stacked horizontal bar chart
    fig, ax = plt.subplots(figsize=(6, 4))

    # Stack the bars
    ax.barh(df['Country.Region'], df['Active_Rate'], label='Active Rate', color='#5e819d')
    ax.barh(df['Country.Region'], df['Deaths_Rate'], left=df['Active_Rate'], label='Deaths Rate', color='#a03623')
    ax.barh(df['Country.Region'], df['Recovered_Rate'], left=df['Active_Rate'] + df['Deaths_Rate'], label='Recovered Rate', color='#76cd26')

    # Reverse the order to have the highest at the top
    ax.invert_yaxis()

    # Set x-axis labels and range
    ax.set_xlabel('Fraction of population')
    ax.set_xlim(0, max_percentage * 1.1 if max_percentage > 0 else 5)
    xticks = np.arange(0, max_percentage * 1.1, 0.2)
    ax.set_xticks(xticks)
    ax.set_xticklabels([f"{tick:.1f}" for tick in xticks])

    # Add title
    ax.set_title('Top most Populated Countries by COVID-19 Total Rates')
 
    # Add legend inside the graph
    ax.legend(loc='lower right', ncol=1)

    # Show plot
    plt.tight_layout()
    plt.show()

db_conn = get_db_conn()  
plot_covid_cases_rate(db_conn)
db_conn.close()