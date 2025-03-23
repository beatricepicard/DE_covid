import streamlit as st

from line_chart import line_chart2
from maps import continent_map 


def continent_data(data, connection, continent , start_date_dt, end_date_dt):
            st.header(continent)
            col1, col2= st.columns([1,1])
            continent_data = data[data["Continent"] == continent].groupby("Date")[["Daily New Cases", "Daily New Deaths", "Daily New Recoveries", "Confirmed", "Deaths", "Recovered"]].sum().reset_index()

            with col1: 
                line_chart2(continent_data, continent)  

            with col2: 
                #Create Continent Map 
                col_metrics1, col_metrics2, col_metrics3 = st.columns(3)
                with col_metrics1:
                    with st.container():
                        st.metric(label="Total Confirmed Cases", value=f"{int(continent_data['Confirmed'].max()):,}")
                with col_metrics2:
                    with st.container():
                        st.metric(label="Total Deaths", value=f"{int(continent_data['Deaths'].max()):,}")
                with col_metrics3:
                    with st.container():
                        st.metric(label="Total Recoveries", value=f"{int(continent_data['Recovered'].max()):,}")
                
        
                with st.container():
                    if continent == "Australia/Oceania":
                        st.warning("No map available for Australia/Oceania.")
                    else:
                        min_date = start_date_dt
                        max_date = end_date_dt
                        continent_date = st.slider("Select a date:", min_value = start_date_dt, max_value = end_date_dt, value = start_date_dt)
                        continent_map(connection, continent, continent_date)