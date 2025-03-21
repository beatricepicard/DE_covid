import streamlit as st
import pandas as pd
import datetime


def date(df):
    date_range = st.sidebar.date_input("Select Date Range:", [df["Date"].min(), df["Date"].max()], min_value=df["Date"].min(), max_value=df["Date"].max())
    start_date, end_date = pd.to_datetime(date_range)
    # Different format needed for SIR-model
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Different format needed for sliders in maps
    start_date_dt = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date_dt = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

    return date_range, start_date, end_date, start_date_str, end_date_str, start_date_dt, end_date_dt