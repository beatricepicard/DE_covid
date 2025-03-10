import streamlit as st
import sqlite3 


st.set_page_config(page_title = "Summary of Covid-Data", layout = "wide", initial_sidebar_state = "expanded")

st.title("Summary of Covid-Data")

with st.sidebar:
    st.title("This is the title of the sidebar")
    st.write("This is the content of the sidebar")

# connection to the database
connection = sqlite3.connect("../data/covid_database.db")


from maps import continent_map, world_map

world_map(connection)

continent = st.selectbox(
    "Select a continent",
    {"Europe", "Asia", "Africa", "North America", "South America"}
)

continent_map(connection, continent)
