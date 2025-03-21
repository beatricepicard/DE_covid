import streamlit as st
import pandas as pd
import datetime


def date(df):
    start_date = st.sidebar.date_input("Start Date:", df["Date"].min(), min_value=df["Date"].min(), max_value=df["Date"].max())
    end_date = st.sidebar.date_input("End Date:", df["Date"].max(), min_value=df["Date"].min(), max_value=df["Date"].max()) 

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if end_date <= start_date:
        st.sidebar.error("End date must fall after start date.")

    # Different format needed for SIR-model
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Different format needed for sliders in maps
    start_date_dt = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date_dt = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

    return start_date, end_date, start_date_str, end_date_str, start_date_dt, end_date_dt