#libraries
import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px
import matplotlib.dates as mdates

#functions
from line_chart import line_chart, line_chart2
from maps import continent_map, world_map
from cases_rates import get_cases_rates
from continent_rate_comparison import get_continent_rates
from design import design_global, design_continent
from organizing_data import data
from date import date
from sir_model import sir_model

# Streamlit Pages Layout 
st.set_page_config(layout = "wide")

#Sample data
db_path = "../data/covid_database.db"
connection = sqlite3.connect(db_path)
df = pd.read_sql("SELECT Date, Country, Continent, Confirmed, Deaths, Recovered FROM new_complete", connection)

#"organizing data"
df = data(df)

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
    connection = sqlite3.connect(db_path)
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

#Page 2: Continent/Country Data
elif st.session_state['page'] == 'continent':
    tab1, tab2, tab3 = st.tabs(["Continent Data", "Country Data", "SIR-Model"])
    continent = st.session_state.get('continent')
    countries_by_continent = sorted(df[df["Continent"] == continent]["Country"].dropna().unique())
    default_country = countries_by_continent[0] if countries_by_continent else "Select a country"
    country = st.sidebar.selectbox( "Select Country", list(countries_by_continent), index=countries_by_continent.index(st.session_state["country"]) if st.session_state["country"] in countries_by_continent else 0)
    st.session_state["country"] = country

    if not continent:
        st.session_state['page'] = "worldwide"
        st.rerun()

#Page2.1: Continent Data
    with tab1:
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
                    st.metric(label="Total Recovered Cases", value=f"{int(continent_data['Recovered'].max()):,}")
            
    
            with st.container():
                if continent == "Australia/Oceania":
                    st.warning("No map available for Australia/Oceania.")
                else:
                    min_date = start_date_dt
                    max_date = end_date_dt
                    continent_date = st.slider("Select a date:", min_value = start_date_dt, max_value = end_date_dt, value = start_date_dt)
                    continent_map(connection, continent, continent_date)

#Page2.2: Country Data
    with tab2:
        col6 = st.columns(1)[0] 
        with col6:
            #line charts for country
            st.header(f"COVID-19 Data for {country}")
            country_data = data[data["Country"] == country].groupby("Date")[["Daily New Cases", "Daily New Deaths", "Daily New Recoveries", "Confirmed", "Deaths", "Recovered"]].sum().reset_index()
            line_chart(country_data, country)

        #COUNTRY COMPARISON (CASES PER 1 MILLION PEOPLE) FOR CHOSEN CONTINENT
        col7 = st.columns(1)[0] 
        with col7: 
            st.markdown(f"### Top 10 Countries of {continent} including {country}")
            col1, col2, col3 = st.columns(3)
            df_rates = get_cases_rates(connection, start_date_str, end_date_str, continent)
            num_countries = len(df_rates)
            if num_countries <= 15:
                top_n = num_countries
            else: 
                top_n = 15
            
            df_rates = df_rates.sort_values(by='ConfirmedPerPop_diff', ascending=True).head(top_n)
            
            if country not in df_rates["Country"].values:
                country_data = get_cases_rates(connection, start_date_str, end_date_str, continent).query(f"Country == '{country}'")
                df_rates = pd.concat([df_rates, country_data])

            df_rates["Country"] = pd.Categorical(df_rates["Country"], categories=df_rates["Country"], ordered=True)
            countries_list = df_rates["Country"].tolist()

            confirmed_color = ["#D9F0A3" if c == country else "#41B6C4" for c in df_rates["Country"]]
            deaths_color = ["#D9F0A3" if c == country else "#78C679" for c in df_rates["Country"]]
            recovered_color = ["#D9F0A3" if c == country else "#ADDD8E" for c in df_rates["Country"]]

            with col1:
                fig1 = px.bar(df_rates, y="Country", x="ConfirmedPerPop_diff", orientation="h", title="Confirmed per 1 million people", color=df_rates["Country"], color_discrete_sequence=confirmed_color)
                fig1.update_layout(showlegend=False, height=300, margin=dict(t=30, b=0, l=0, r=20))
                fig1.update_xaxes(dict(range=[0, df_rates["ConfirmedPerPop_diff"].max() * 1.1]), showticklabels=False, title="")
                fig1.update_yaxes(title="", categoryorder="array", categoryarray=countries_list, tickfont=dict(size=12), tickangle=0, tickmode='linear')
                fig1.update_traces(texttemplate='%{x:.0f}', textposition='outside',cliponaxis=False) 
                st.plotly_chart(fig1, use_container_width=True)
                
            with col2:
                fig2 = px.bar(df_rates, y="Country", x="DeathsPerPop_diff", orientation="h", title="Deaths per 1 million people", color=df_rates["Country"], color_discrete_sequence= deaths_color)
                fig2.update_layout(showlegend=False, height=300, margin=dict(t=30, b=0, l=0, r=20))
                fig2.update_xaxes(dict(range=[0, df_rates["DeathsPerPop_diff"].max() * 1.1]), showticklabels=False, title="")
                fig2.update_yaxes(title="", categoryorder="array", categoryarray=countries_list, tickfont=dict(size=12), tickangle=0, tickmode='linear')
                fig2.update_traces(texttemplate='%{x:.0f}', textposition='outside',cliponaxis=False)
                st.plotly_chart(fig2, use_container_width=True)

            with col3:
                fig3 = px.bar(df_rates, y="Country", x="RecoveredPerPop_diff", orientation="h", title="Recovered per 1 million people", color=df_rates["Country"], color_discrete_sequence= recovered_color)
                fig3.update_layout(showlegend=False, height=300, margin=dict(t=30, b=0, l=0, r=20))
                fig3.update_xaxes(dict(range=[0, df_rates["RecoveredPerPop_diff"].max() * 1.1]), showticklabels=False, title="")
                fig3.update_yaxes(title="", categoryorder="array", categoryarray=countries_list, tickfont=dict(size=12), tickangle=0, tickmode='linear')
                fig3.update_traces(texttemplate='%{x:.0f}', textposition='outside',cliponaxis=False)
                st.plotly_chart(fig3, use_container_width=True)


#Page2.3: SIR-Model
    with tab3:
        sir_model(connection, country, start_date, end_date)


#Back to Glonbal Data Button @Sidebar
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