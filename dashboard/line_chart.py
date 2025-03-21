import streamlit as st
import pandas as pd
import plotly.express as px

def line_chart(data, scope_title):

    col1, col2, col3 = st.columns(3)

    with col1:
        fig_cases = px.line(data, x="Date", y="Daily New Cases", title="Daily New Cases", color_discrete_sequence= ["#41B6C4"], line_shape='spline')
        st.plotly_chart(fig_cases, use_container_width=True)

    with col2:
        fig_deaths = px.line(data, x="Date", y="Daily New Deaths", title="Daily New Deaths", color_discrete_sequence= ["#78C679"], line_shape='spline')
        st.plotly_chart(fig_deaths, use_container_width=True)

    with col3:
        fig_recoveries = px.line(data, x="Date", y="Daily New Recoveries", title="Daily New Recoveries", color_discrete_sequence=["#ADDD8E"], line_shape='spline')
        st.plotly_chart(fig_recoveries, use_container_width=True)

    # Display total numbers
    st.markdown(f"### Total Numbers - {scope_title}")

    with st.container():
            col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
            with col_metrics1:
                with st.container():
                    st.metric(label="Total Confirmed Cases", value=f"{data['Confirmed'].max():,}")
            with col_metrics2:
                with st.container():
                    st.metric(label="Total Deaths", value=f"{data['Deaths'].max():,}")
            with col_metrics3:
                with st.container():
                    st.metric(label="Total Recovered Cases", value=f"{data['Recovered'].max():,}")

    # Display cumulative line charts

    col4, col5, col6 = st.columns(3)

    with col4:
        fig_total_cases = px.line(data, x="Date", y="Confirmed", title="Total Confirmed Cases", color_discrete_sequence= ["#41B6C4"], line_shape='spline')
        st.plotly_chart(fig_total_cases, use_container_width=True)

    with col5:
        fig_total_deaths = px.line(data, x="Date", y="Deaths", title="Total Deaths", color_discrete_sequence=["#78C679"] , line_shape='spline')
        st.plotly_chart(fig_total_deaths, use_container_width=True)

    with col6:
        fig_total_recovered = px.line(data, x="Date", y="Recovered", title="Total Recovered Cases", color_discrete_sequence= ["#ADDD8E"], line_shape='spline')
        st.plotly_chart(fig_total_recovered, use_container_width=True)
