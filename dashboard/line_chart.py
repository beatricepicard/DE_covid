import streamlit as st
import plotly.express as px

def line_chart(data, scope_title):

    col1, col2, col3 = st.columns(3)

    with col1:
        fig_cases = px.line(data, x="Date", y="Daily New Cases", title="Daily New Cases", color_discrete_sequence= ["#41B6C4"], line_shape='spline')
        fig_cases.update_layout(height=200, margin=dict(t=23, b=0, l=10, r=10), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_cases, use_container_width=True)

    with col2:
        fig_deaths = px.line(data, x="Date", y="Daily New Deaths", title="Daily New Deaths", color_discrete_sequence= ["#78C679"], line_shape='spline')
        fig_deaths.update_layout(height=200, margin=dict(t=23, b=0, l=10, r=10), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_deaths, use_container_width=True)

    with col3:
        fig_recoveries = px.line(data, x="Date", y="Daily New Recoveries", title="Daily New Recoveries", color_discrete_sequence=["#ADDD8E"], line_shape='spline')
        fig_recoveries.update_layout(height=200, margin=dict(t=23, b=0, l=10, r=10), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_recoveries, use_container_width=True)

    # Display total numbers
    # st.markdown(f"### Total Numbers - {scope_title}")

    with st.container():
            col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
            with col_metrics1:
                with st.container():
                    st.metric(label="Total Confirmed Cases", value=f"{int(data['Confirmed'].max()):,}")
            with col_metrics2:
                with st.container():
                    st.metric(label="Total Deaths", value=f"{int(data['Deaths'].max()):,}")
            with col_metrics3:
                with st.container():
                    st.metric(label="Total Recoveries", value=f"{int(data['Recovered'].max()):,}")

    # Display cumulative line charts

    col4, col5, col6 = st.columns(3)

    with col4:
        fig_total_cases = px.line(data, x="Date", y="Confirmed", title="Total Confirmed Cases", color_discrete_sequence= ["#41B6C4"], line_shape='spline')
        fig_total_cases.update_layout(height=200, margin=dict(t=23, b=0, l=10, r=10), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_total_cases, use_container_width=True)

    with col5:
        fig_total_deaths = px.line(data, x="Date", y="Deaths", title="Total Deaths", color_discrete_sequence=["#78C679"] , line_shape='spline')
        fig_total_deaths.update_layout(height=200, margin=dict(t=23, b=0, l=10, r=10), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_total_deaths, use_container_width=True)

    with col6:
        fig_total_recovered = px.line(data, x="Date", y="Recovered", title="Total Recoveries", color_discrete_sequence= ["#ADDD8E"], line_shape='spline')
        fig_total_recovered.update_layout(height=200, margin=dict(t=23, b=0, l=10, r=10), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_total_recovered, use_container_width=True)


def line_chart2(data, scoop_title): 

    col1, col2 = st.columns([1, 1])

    with col1:
        fig_cases = px.line(data, x="Date", y="Daily New Cases", title="Daily New Cases", color_discrete_sequence= ["#41B6C4"], line_shape='spline')
        fig_cases.update_layout(height=202, margin=dict(t=40, b=10, l=15, r=15), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_cases, use_container_width=True)

    with col2:
        fig_total_cases = px.line(data, x="Date", y="Confirmed", title="Total Confirmed Cases", color_discrete_sequence= ["#41B6C4"], line_shape='spline')
        fig_total_cases.update_layout(height=202, margin=dict(t=40, b=10, l=15, r=15), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_total_cases, use_container_width=True)


    # Display cumulative line charts
    col4, col5 = st.columns([1,1])

    with col4:
        fig_deaths = px.line(data, x="Date", y="Daily New Deaths", title="Daily New Deaths", color_discrete_sequence= ["#78C679"], line_shape='spline')
        fig_deaths.update_layout(height=202, margin=dict(t=40, b=10, l=15, r=15), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_deaths, use_container_width=True)


    with col5:
        fig_total_deaths = px.line(data, x="Date", y="Deaths", title="Total Deaths", color_discrete_sequence=["#78C679"] , line_shape='spline')
        fig_total_deaths.update_layout(height=202, margin=dict(t=40, b=10, l=15, r=15), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_total_deaths, use_container_width=True)

    col6, col7 = st.columns([1,1])

    with col6:
        fig_recoveries = px.line(data, x="Date", y="Daily New Recoveries", title="Daily New Recoveries", color_discrete_sequence=["#ADDD8E"], line_shape='spline')
        fig_recoveries.update_layout(height=202, margin=dict(t=40, b=10, l=15, r=15), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_recoveries, use_container_width=True)
    
    with col7:
        fig_total_recovered = px.line(data, x="Date", y="Recovered", title="Total Recoveries", color_discrete_sequence= ["#ADDD8E"], line_shape='spline')
        fig_total_recovered.update_layout(height=202, margin=dict(t=40, b=10, l=15, r=15), xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_total_recovered, use_container_width=True)



