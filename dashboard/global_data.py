import streamlit as st
import plotly.express as px

from line_chart import line_chart
from maps import world_map
from continent_rate_comparison import get_continent_rates

def global_data(data, db_path, connection, start_date, end_date, start_date_dt, end_date_dt):
    st.title("COVID-19 Dashboard")
    st.header("Global Data")

    world_data = data.groupby("Date")[["Daily New Cases", "Daily New Deaths", "Daily New Recoveries", "Confirmed", "Deaths", "Recovered"]].sum().reset_index()
    scope_title = "global"
    line_chart(world_data, scope_title)

    col1 = st.columns(1)
    with col1[0]:
        min_date = start_date_dt
        max_date = end_date_dt
            # Slider for date selection
        date = st.slider("Select a date:", min_value=min_date, max_value=max_date, value=min_date, key="map_slider")    
            # Plotting the map
        world_map(connection, date)


        #CONTINENT COMPARISON (CASES PER 1 MILLION PEOPLE)
        col1, col2, col3 = st.columns(3)
        df_continents = get_continent_rates(connection, start_date, end_date).sort_values(by='ConfirmedPerPop_diff', ascending=True)

        with col1:
            fig1 = px.bar(df_continents, x="ConfirmedPerPop_diff", y="Continent", title="Confirmed per 1 million people", text_auto=".0f", orientation='h')
            fig1.update_traces(marker_color="#41B6C4", textposition='outside', cliponaxis=False) 
            fig1.update_layout(xaxis=dict(title="", showticklabels=False), yaxis=dict(title=""), height = 250, margin=dict(t=30, b=0, l=0, r=40))
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = px.bar(df_continents, x="DeathPerPop_diff", y="Continent", title="Deaths per 1 million people", text_auto=".0f", orientation='h')
            fig2.update_traces(marker_color="#78C679", textposition='outside', cliponaxis=False) 
            fig2.update_layout(xaxis=dict(title="", showticklabels=False), yaxis=dict(title=""), height = 250, margin=dict(t=30, b=0, l=0, r=40))
            st.plotly_chart(fig2, use_container_width=True)

        with col3:
            fig3 = px.bar(df_continents, x="RecoveredPerPop_diff", y="Continent", title="Recovered per 1 million people", text_auto=".0f", orientation='h')
            fig3.update_traces(marker_color="#ADDD8E", textposition='outside', cliponaxis=False) 
            fig3.update_layout(xaxis=dict(title="", showticklabels=False), yaxis=dict(title=""), height = 250, margin=dict(t=30, b=0, l=0, r=40))
            st.plotly_chart(fig3, use_container_width=True)