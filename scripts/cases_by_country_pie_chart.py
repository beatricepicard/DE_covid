import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_db_conn():
    path = r"..\data\covid_database.db"
    conn = sqlite3.connect(path)
    return conn

def plot_covid_pie_chart(conn, country):
    query = '''
        SELECT cw.Active, cw.Deaths, cw.Recovered, wd.Population 
        FROM country_wise cw
        JOIN worldometer_data wd ON cw."Country.Region" = wd."Country.Region"
        WHERE cw."Country.Region" = ?
    '''
    db_cursor = conn.execute(query, (country,))
    data = db_cursor.fetchone()
    
    if not data:
        print(f"No data found for {country}")
        return
    
    active, deaths, recovered, population = data
    
    if population is None or population == 0:
        print(f"Invalid population data for {country}")
        return
    
    confirmed_cases = active + deaths + recovered
    
    labels = [f'{active}', f'{deaths}', f'{recovered}']
    sizes = [active, deaths, recovered]
    colors = ['silver', 'red', 'limegreen']
    fig, ax = plt.subplots(figsize=(6, 4))
    wedges, texts = ax.pie(sizes, labels=labels, colors=colors, startangle=140,
                            wedgeprops={'width': 0.4}, pctdistance=0.55)
    
    plt.text(0, 0, confirmed_cases, horizontalalignment='center', verticalalignment='center', 
             fontsize=18, fontweight='bold')
    
    ax.legend(['Active', 'Deaths', 'Recovered'], loc="lower center", ncol=3)
    plt.title(f'COVID-19 Cases in {country}')
    plt.show()

db_conn = get_db_conn() 
plot_covid_pie_chart(db_conn, 'Austria')
db_conn.close()