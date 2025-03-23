#libraries
import streamlit as st
import pandas as pd
import sqlite3
import os

#functions
from design import design_global, design_continent
from organizing_data import organizing_data
from date import date
from sir_model import sir_model
from global_data import global_data
from continent_data import continent_data
from country_data import country_data

# Streamlit Pages Layout 
st.set_page_config(layout = "wide")

#Sample data
db_path = os.path.join(os.path.dirname(__file__), 'covid_database.db')
connection = sqlite3.connect(db_path)
df = pd.read_sql("SELECT Date, Country, Continent, Confirmed, Deaths, Recovered FROM new_complete", connection)

#"organizing data"
df = organizing_data(df)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state['page'] = 'worldwide'
if 'continent' not in st.session_state:
    st.session_state['continent'] = None
if 'country' not in st.session_state:
    st.session_state['country'] = None

# Sidebar Filters
st.sidebar.title("Filters")

#date selection
start_date, end_date, start_date_str, end_date_str, start_date_dt, end_date_dt = date(df)

data = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
continents = sorted(df["Continent"].dropna().unique())

#Continent selection
continent = st.sidebar.selectbox("Select Continent", ["the world"] + list(continents), index=(continents.index(st.session_state["continent"]) + 1) if st.session_state["continent"] else 0)
if continent != "the world" and continent != st.session_state["continent"]:
    st.session_state['continent'] = continent
    st.session_state['page'] = 'continent'
    st.rerun()

#Page 1: Worldwide data
if st.session_state['page'] == 'worldwide':
    global_data(data, db_path, connection, start_date, end_date, start_date_dt, end_date_dt)

#Page 2: Continent/Country Data
elif st.session_state['page'] == 'continent':

    tab1, tab2, tab3 = st.tabs(["Continent Data", "Country Data", "SIR-Model"])
    countries_by_continent = sorted(df[df["Continent"] == continent]["Country"].dropna().unique())
    default_country = countries_by_continent[0] if countries_by_continent else "Select a country"
    country = st.sidebar.selectbox( "Select Country", list(countries_by_continent), index=countries_by_continent.index(st.session_state["country"]) if st.session_state["country"] in countries_by_continent else 0)
    st.session_state["country"] = country

    if continent == "the world":
        st.session_state['page'] = "worldwide"
        st.rerun()

#Page2.1: Continent Data
    with tab1:
        continent_data(data, connection, continent, start_date_dt, end_date_dt)

#Page2.2: Country Data
    with tab2:
        country_data(data, connection, start_date_str, end_date_str, continent, country)


#Page2.3: SIR-Model
    with tab3:
        sir_model(connection, country, start_date, end_date)


#Back to Global Data Button @Sidebar
st.sidebar.write("---")
if st.sidebar.button("Back to Global Data"):
    st.session_state['page'] = 'worldwide'
    st.session_state['continent'] = None
    st.session_state["country"] = None
    st.rerun()


#design-stuff
if st.session_state['page'] == "worldwide":
    design_global()
else:
    design_continent()

connection.close()                                          