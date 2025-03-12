import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title = "Summary of Covid-Data", layout = "wide", initial_sidebar_state = "expanded")

st.title("Covid confirmed, deaths cases by Continent, %% of population")

with st.sidebar:
    st.title("This is the title of the sidebar")
    st.write("This is the content of the sidebar")

chosen_date = st.date_input("Select Date", pd.to_datetime('2020-04-10'))

path = "C:\My documents\VUA\Data engineering\Project\Github_clone\DE_covid\data\covid_database.db"
conn = sqlite3.connect(path)

tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql_query(tables_query, conn)

print(tables)

sql_query = f"""
SELECT
    w.Continent,
    SUM(c.Confirmed) AS Total_Confirmed,
    SUM(c.Deaths) AS Total_Deaths,
    SUM(w.Population) AS Total_Population,
    SUM(c.Confirmed) * 1.0 / SUM(w.Population) * 100 AS Confirmed_Rate,
    SUM(c.Deaths) * 1.0 / SUM(w.Population) * 100 AS Deaths_Rate
FROM
    complete c
JOIN
    worldometer_data w ON c."Country.Region" = w."Country.Region"
WHERE
    c.Date = '{chosen_date}'
GROUP BY
    w.Continent
ORDER BY
    Confirmed_Rate ASC;
"""
continent_data = pd.read_sql_query(sql_query, conn)
conn.close()

fig, ax = plt.subplots(figsize=(10, 4))
continent_data.set_index('Continent')[['Confirmed_Rate', 'Deaths_Rate']].plot(kind='barh', stacked=True, ax=ax)

ax.set_xlabel("Rate (%) of Population")
ax.set_title(f"Confirmed and Deaths Rates by Continent on {chosen_date.strftime('%Y-%m-%d')}")
ax.legend(loc='lower right')

# Show the plot in Streamlit
st.pyplot(fig)