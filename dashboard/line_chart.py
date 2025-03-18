import streamlit as st
import pandas as pd
import plotly.express as px

def line_chart(data, scope_title):
    st.markdown(f"### Daily Trends - {scope_title}")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Daily New Cases")
        fig_cases = px.line(data, x="Date", y="Daily New Cases", title="Daily New Cases", color_discrete_sequence=["blue"], line_shape='spline')
        st.plotly_chart(fig_cases, use_container_width=True)

    with col2:
        st.markdown("#### Daily New Deaths")
        fig_deaths = px.line(data, x="Date", y="Daily New Deaths", title="Daily New Deaths", color_discrete_sequence=["red"], line_shape='spline')
        st.plotly_chart(fig_deaths, use_container_width=True)

    with col3:
        st.markdown("#### Daily New Recoveries")
        fig_recoveries = px.line(data, x="Date", y="Daily New Recoveries", title="Daily New Recoveries", color_discrete_sequence=["green"], line_shape='spline')
        st.plotly_chart(fig_recoveries, use_container_width=True)

    # Display total numbers
    st.markdown(f"### Total Numbers - {scope_title}")

    col_metrics1, col_metrics2, col_metrics3 = st.columns(3)

    with col_metrics1:
        st.metric(label="Total Confirmed Cases", value=f"{data['Confirmed'].max():,}")

    with col_metrics2:
        st.metric(label="Total Deaths", value=f"{data['Deaths'].max():,}")

    with col_metrics3:
        st.metric(label="Total Recovered Cases", value=f"{data['Recovered'].max():,}")

    # Display cumulative line charts
    st.markdown(f"### Cumulative Trends - {scope_title}")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("#### Total Confirmed Cases")
        fig_total_cases = px.line(data, x="Date", y="Confirmed", title="Total Confirmed Cases", color_discrete_sequence=["blue"], line_shape='spline')
        st.plotly_chart(fig_total_cases, use_container_width=True)

    with col5:
        st.markdown("#### Total Deaths")
        fig_total_deaths = px.line(data, x="Date", y="Deaths", title="Total Deaths", color_discrete_sequence=["red"], line_shape='spline')
        st.plotly_chart(fig_total_deaths, use_container_width=True)

    with col6:
        st.markdown("#### Total Recovered Cases")
        fig_total_recovered = px.line(data, x="Date", y="Recovered", title="Total Recovered Cases", color_discrete_sequence=["green"], line_shape='spline')
        st.plotly_chart(fig_total_recovered, use_container_width=True)
