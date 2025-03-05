
import streamlit as st

st.set_page_config(page_title = "Summary of Covid-Data", layout = "wide", initial_sidebar_state = "expanded")

st.title("Summary of Covid-Data")

with st.sidebar:
    st.title("This is the title of the sidebar")
    st.write("This is the content of the sidebar")
