import streamlit as st
st.set_page_config(layout = "wide")
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px
import datetime
from aggregation import aggregation
from country_summary import country_summary
from get_countries import get_countries
from line_chart import line_chart
from functions_dashboard import calculate_sir_parameters 
from maps import continent_map, world_map
from cases_rates import get_cases_rates
from continent_rate_comparison import get_continent_rates
import pycountry_convert as pc
import matplotlib.dates as mdates

def get_continent(country_name):
    try:
        country_code = pc.country_name_to_country_alpha2(country_name, cn_name_format="default")
        continent_code = pc.country_alpha2_to_continent_code(country_code)
        continent_names = {
            "AF": "Africa",
            "AS": "Asia",
            "EU": "Europe",
            "NA": "North America",
            "SA": "South America",
            "OC": "Oceania"
        }
        return continent_names.get(continent_code, "Unknown")
    except:
        return "Unknown"

#Sample data
db_path = "../data/covid_database.db"
connection = sqlite3.connect(db_path)

df = pd.read_sql("SELECT Date, `Country.Region`, Confirmed, Deaths, Recovered FROM complete ORDER BY Date", connection)
# Change date
df["Date"] = pd.to_datetime(df["Date"])

# Calculate daily changes
df["Daily New Cases"] = df.groupby(["Country.Region"])["Confirmed"].diff().fillna(0)
df["Daily New Deaths"] = df.groupby(["Country.Region"])["Deaths"].diff().fillna(0)
df["Daily New Recoveries"] = df.groupby(["Country.Region"])["Recovered"].diff().fillna(0)

# Avoid negative values
df["Daily New Cases"] = df["Daily New Cases"].clip(lower=0)
df["Daily New Deaths"] = df["Daily New Deaths"].clip(lower=0)
df["Daily New Recoveries"] = df["Daily New Recoveries"].clip(lower=0)

#Assign Continents
df["Continent"] = df["Country.Region"].apply(get_continent)

# Streamlit Pages Layout
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
date_range = st.sidebar.date_input("Select Date Range:", [df["Date"].min(), df["Date"].max()], min_value=df["Date"].min(), max_value=df["Date"].max())
start_date, end_date = pd.to_datetime(date_range)
# Different format needed for SIR-model
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime("%Y-%m-%d")

# Different format needed for sliders in maps
start_date_dt = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
end_date_dt = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

data = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
available_continents = sorted(df["Continent"].dropna().unique())
available_continents = [c for c in available_continents if c != "Unknown"]

#Continent selection
continent = st.sidebar.selectbox("Select Continent", ["Select a continent"] + list(available_continents), index=(available_continents.index(st.session_state["continent"]) + 1) if st.session_state["continent"] else 0)
if continent != "Select a continent" and continent != st.session_state["continent"]:
    st.session_state['continent'] = continent
    st.session_state['page'] = 'continent'
    st.rerun()

#Page 1: Worldwide data
if st.session_state['page'] == 'worldwide':
    st.title("COVID-19 Dashboard")
    st.header("Worldwide Data")

    col1, col2 = st.columns([3,2])
    
    with col1:
        world_data = data.groupby("Date")[["Daily New Cases", "Daily New Deaths", "Daily New Recoveries", "Confirmed", "Deaths", "Recovered"]].sum().reset_index()
        scope_title = "Worldwide"
        line_chart(world_data, scope_title)

    with col2:
        # Create world map
        min_date = start_date_dt
        max_date = end_date_dt
        date = st.slider("Select a date:", min_value = min_date, max_value = max_date, value = min_date)
        world_map(connection, date)

        #CONTINENT COMPARISON (CASES PER 1 MILLION PEOPLE)
        st.markdown("### Continent comparison")
        col1, col2, col3 = st.columns(3)
        connection = sqlite3.connect(db_path)
        df_continents = get_continent_rates(connection, start_date, end_date).sort_values(by='ConfirmedPerPop_diff', ascending=True)

        with col1:
            fig1 = px.bar(df_continents, x="ConfirmedPerPop_diff", y="Continent", title="Confirmed per 1 million people", orientation='h')
            fig1.update_traces(marker_color="#41B6C4")  # Set color properly
            fig1.update_layout(xaxis=dict(title="", showticklabels=False), yaxis=dict(title=""))
            st.plotly_chart(fig1, use_container_width=True)

        with col2:
            fig2 = px.bar(df_continents, x="DeathPerPop_diff", y="Continent", title="Deaths per 1 million people", text_auto=".0f", orientation='h')
            fig2.update_traces(marker_color="#78C679")  # Set color properly
            fig2.update_layout(xaxis=dict(title="", showticklabels=False), yaxis=dict(title=""))
            st.plotly_chart(fig2, use_container_width=True)

        with col3:
            fig3 = px.bar(df_continents, x="RecoveredPerPop_diff", y="Continent", title="Recovered per 1 million people", text_auto=".0f", orientation='h')
            fig3.update_traces(marker_color="#ADDD8E")  # Set color properly
            fig3.update_layout(xaxis=dict(title="", showticklabels=False), yaxis=dict(title=""))
            st.plotly_chart(fig3, use_container_width=True)


#Page 2: Continent/ Country data
elif st.session_state['page'] == 'continent':
    st.title("COVID-19 Data")
    continent = st.session_state.get('continent')
    if not continent:
        st.session_state['page'] = "worldwide"
        st.rerun()
    
    countries_by_continent = sorted(df[df["Continent"] == continent]["Country.Region"].dropna().unique())
    default_country = countries_by_continent[0] if countries_by_continent else "Select a country"
    country = st.sidebar.selectbox( "Select Country", list(countries_by_continent), index=countries_by_continent.index(st.session_state["country"]) if st.session_state["country"] in countries_by_continent else 0)

    st.session_state["country"] = country

    col1, col2= st.columns([1,1])

    with col1: 
        st.header(f"{continent} Data")

        #Line charts for continent
        continent_data = data[data["Continent"] == continent].groupby("Date")[["Daily New Cases", "Daily New Deaths", "Daily New Recoveries", "Confirmed", "Deaths", "Recovered"]].sum().reset_index()
        line_chart(continent_data, continent)  

    with col2: 
        #Create Continent Map 
        if continent == "Oceania":
            st.warning("No map available for Oceania.")
        else:
            min_date = start_date_dt
            max_date = end_date_dt
            continent_date = st.slider("Select a date:", min_value = start_date_dt, max_value = end_date_dt, value = start_date_dt)
            continent_map(connection, continent, continent_date)

        #SIR-Model per country
        # Get dataframe from database
        query_combine = "SELECT * FROM new_complete"
        df_sir = pd.read_sql(query_combine, connection)

        df_sir["Susceptible"] = df_sir["Population"] - df_sir["Active"].fillna(0) - df_sir["Deaths"].fillna(0) - df_sir["Recovered"].fillna(0)
        df_sir["mu"] = float("nan")
        df_sir["gamma"] = 1 / 4.5
        df_sir["beta"] = float("nan")
        df_sir["alpha"] = float("nan")
        df_sir["R0"] = float("nan")

        st.header("The SIR Model")
        with st.expander("Click for explanation"):
            st.text("The spread of epidemics is often described using the SIR model, which tracks individuals in a population as Susceptible (S), Infected (I), or Recovered (R). In this case, an additional category is included: Deceased (D).")
            st.text("Each day, individuals can either remain in their current state or transition to an adjacent state. For example, an infected person can recover, succumb to the disease, or stay infected, while a deceased individual remains in that state permanently.")
            st.text("The daily changes in the population are governed by the following equations:")
            st.latex(r"\Delta S(t) = \alpha R(t) - \beta S(t) \frac{I(t)}{N}")
            st.latex(r"\Delta I(t) = \beta S(t) \frac{I(t)}{N} - \mu I(t) - \gamma I(t)")
            st.latex(r"\Delta R(t) = \gamma I(t) - \alpha R(t)")
            st.latex(r"\Delta D(t) = \mu I(t)")
            st.text("By estimating the parameters for each country, we can fill in missing values, leading to better predictive performance.")
            st.subheader("What is R0?")
            st.text("R0, or the basic reproduction number, represents the average number of secondary infections generated by a single infected individual in a completely susceptible population.")
            st.text("If R0 > 1, the infection can spread in the population. If R0 < 1, the infection will eventually die out.")

        # Columns for SIR parameters and R0 chart
        col4, col5 = st.columns([1, 1], gap="medium")
        with col4:
            if country:
                try:
                    df_sir = calculate_sir_parameters(country, df_sir)
                    country_params = df_sir[df_sir["Country"] == country]

                    st.subheader(f"Parameters for {country}")
                    st.write(f"**Adjustment Factor (α):** {country_params['alpha'].values[0]:.4f}")
                    st.write(f"**Transmission Rate (β):** {country_params['beta'].values[0]:.4f}")
                    st.write(f"**Recovery Rate (γ):** {country_params['gamma'].values[0]:.4f}")
                    st.write(f"**Mortality Rate (μ):** {country_params['mu'].values[0]:.4f}")
                except Exception as e:
                    st.error(f"Error calculating parameters for {country}: {str(e)}")

        with col5:
            st.subheader(f"R0 Over Time for {country}")
            fig, ax = plt.subplots()
            df_sir["Date"] = pd.to_datetime(df_sir["Date"])
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            ax.plot(df_sir["Date"], df_sir["R0"], marker='o', linestyle='-', color= "#225EA8")
            ax.set_xlim(mdates.date2num(start_date), mdates.date2num(end_date))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            plt.xticks(rotation=45)
            ax.set_xlabel("Date")
            ax.set_ylabel("R0")
            ax.set_title(f"R0 Over Time for {country}")
            st.pyplot(fig)

    col6, col7 = st.columns([1,1])
    with col6:
        #line charts for country
        st.header(f"COVID-19 Data for {country}")
        country_data = data[data["Country.Region"] == country].groupby("Date")[["Daily New Cases", "Daily New Deaths", "Daily New Recoveries", "Confirmed", "Deaths", "Recovered"]].sum().reset_index()
        line_chart(country_data, country)

    #COUNTRY COMPARISON (CASES PER 1 MILLION PEOPLE) FOR CHOSEN CONTINENT
    with col7: 
        st.markdown(f"### Countries comparison including {country}")
        #col1, col2, col3 = st.columns(3)
        df_rates = get_cases_rates(connection, start_date_str, end_date_str, continent)
        num_countries = len(df_rates)
        if num_countries <= 20:
            top_n = num_countries
        else: 
            top_n = 20
        
        df_rates = df_rates.sort_values(by='ConfirmedPerPop_diff', ascending=True).head(top_n)
       
        if country not in df_rates["Country"].values:
            country_data = get_cases_rates(connection, start_date, end_date, continent).query(f"Country == '{country}'")
            df_rates = pd.concat([df_rates, country_data])

        df_rates["Country"] = pd.Categorical(df_rates["Country"], categories=df_rates["Country"], ordered=True)
        countries_list = df_rates["Country"].tolist()

        confirmed_color = ["#D9F0A3" if c == country else "#41B6C4" for c in df_rates["Country"]]
        deaths_color = ["#D9F0A3" if c == country else "#78C679" for c in df_rates["Country"]]
        recovered_color = ["#D9F0A3" if c == country else "#ADDD8E" for c in df_rates["Country"]]

        #with col1:
        fig1 = px.bar(df_rates, y="Country", x="ConfirmedPerPop_diff", orientation="h", title="Confirmed per 1 million people", text_auto=".0f", color=df_rates["Country"], color_discrete_sequence=confirmed_color)
        fig1.update_layout(title_x=0.5)
        fig1.update_yaxes(categoryorder="array", categoryarray=countries_list)
        fig1.update_xaxes(title_text="") 
        fig1.update_layout(yaxis_title="") 
        fig1.update_layout(xaxis=dict(range=[0, df_rates["ConfirmedPerPop_diff"].max() * 1.1]))
        st.plotly_chart(fig1)
        
        #with col2:
        fig2 = px.bar(df_rates, y="Country", x="DeathsPerPop_diff", orientation="h", title="Deaths per 1 million people", text_auto=".0f", color=df_rates["Country"], color_discrete_sequence= deaths_color)
        fig2.update_layout(title_x=0.5)
        fig2.update_yaxes(categoryorder="array", categoryarray=countries_list)
        fig2.update_xaxes(title_text="") 
        fig2.update_layout(yaxis_title="") 
        #fig2.update_layout(xaxis=dict(range=[0, df_rates["DeathsPerPop_diff"].max() * 1.1]))
        st.plotly_chart(fig2)

        #with col3:
        fig3 = px.bar(df_rates, y="Country", x="RecoveredPerPop_diff", orientation="h", title="Recovered per 1 million people", text_auto=".0f", color=df_rates["Country"], color_discrete_sequence= recovered_color)
        fig3.update_layout(title_x=0.5)
        fig3.update_yaxes(categoryorder="array", categoryarray=countries_list)
        fig3.update_xaxes(title_text="")  
        fig3.update_layout(yaxis_title="")
        fig3.update_layout(xaxis=dict(range=[0, df_rates["RecoveredPerPop_diff"].max() * 1.1])) 
        st.plotly_chart(fig3)
    
     
    st.sidebar.write("---")
    if st.sidebar.button("Go Back to Worldwide Data"):
        st.session_state['page'] = 'worldwide'
        st.session_state['continent'] = None
        st.session_state["country"] = None
        st.rerun()


#design-stuff
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    body, .stApp {
        background-color: #FFFFFF; /* White background */
        color: #000000; /* Black Text */
        font-family: 'Montserrat', sans-serif; 
    }

    .stSidebar {
    background-color: #F8F8F8; /* Very Light Gray */
    color: #000000; /* Black Text */
    font-family: 'Montserrat', sans-serif;
    }

    .stSelectbox, .stDateInput, .stMetric, .stPlotlyChart {
        background-color: transparent;
        color: #000000; 
        border-radius: none;
        box-shadow: none;
        padding: 8px;
        font-family: 'Montserrat', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 700; /* Bold Headers */
    }

    </style>
    """,
    unsafe_allow_html=True
)
connection.close()                                          