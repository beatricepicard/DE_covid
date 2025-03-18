import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px
from aggregation import aggregation
from country_summary import country_summary
from get_countries import get_countries
from line_chart import line_chart
from functions_dashboard import calculate_sir_parameters 
from get_countries_ import get_countries
from cases_rates import get_cases_rates
from continent_rate_comparison import get_continent_rates


# Verbindung zur Datenbank
db_path = "../data/covid_database.db"
connection = sqlite3.connect(db_path)

# Daten abrufen
df = pd.read_sql("SELECT Date, `Country.Region`, Confirmed, Deaths, Recovered FROM complete ORDER BY Date", connection)

# Datum umwandeln
df["Date"] = pd.to_datetime(df["Date"])

# Tägliche Veränderungen berechnen
df["Daily New Cases"] = df.groupby(["Country.Region"])["Confirmed"].diff().fillna(0)
df["Daily New Deaths"] = df.groupby(["Country.Region"])["Deaths"].diff().fillna(0)
df["Daily New Recoveries"] = df.groupby(["Country.Region"])["Recovered"].diff().fillna(0)

# Negative Werte vermeiden
df["Daily New Cases"] = df["Daily New Cases"].clip(lower=0)
df["Daily New Deaths"] = df["Daily New Deaths"].clip(lower=0)
df["Daily New Recoveries"] = df["Daily New Recoveries"].clip(lower=0)

# Kontinent-Zuordnung
continent_mapping = {
    "USA": "North America", "Canada": "North America", "Mexico": "North America",
    "Germany": "Europe", "France": "Europe", "Italy": "Europe", "Spain": "Europe",
    "India": "Asia", "China": "Asia", "Japan": "Asia", "South Korea": "Asia",
    "Brazil": "South America", "Argentina": "South America", "Colombia": "South America",
    "South Africa": "Africa", "Egypt": "Africa", "Nigeria": "Africa",
    "Australia": "Oceania", "New Zealand": "Oceania"
}

df["Continent"] = df["Country.Region"].map(continent_mapping).fillna("Unknown")

# Streamlit-App-Layout
st.title("COVID-19 Dashboard")

# Sidebar für Filter
st.sidebar.header("Filter Options")

# Datumsbereich auswählen
date_range = st.sidebar.date_input("Select Date Range:", [df["Date"].min(), df["Date"].max()], min_value=df["Date"].min(), max_value=df["Date"].max())
start_date, end_date = pd.to_datetime(date_range)

# Streamlit sidebar for selecting Continent, Country, Start Date, and End Date
st.sidebar.header("Filter Options")
selected_country = st.sidebar.selectbox("Select Country:", countries, index=countries.index("Netherlands")) #setting Netherlands as starting country
date_range = st.sidebar.date_input("Select Date Range:", [min_date, max_date], min_value=min_date, max_value=max_date)
start_date, end_date = pd.to_datetime(date_range)
if start_date > end_date:
    st.sidebar.error("End date must be after start date!")
selected_continent = st.sidebar.selectbox("Select Continent", ["All"] + ["Africa", "Asia", "Europe", "North America", "Oceania", "South America"])
countries = get_countries(connection, selected_continent)
selected_country_2 = st.sidebar.selectbox("Select Country", countries, index=0)

#filtering data based on selected date range and selected country
df_filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
df_country_filtered = df_filtered[df_filtered["Country.Region"] == selected_country]

#worldwide numeric values on dashboard
st.markdown("###Global COVID-19 Statistics") #hashtags makes text appeare smaller
col1, col2, col3, col4 = st.columns(4) #creates 4 colums
col1.metric("Confirmed", f"{df_filtered['Confirmed'].sum():,}")
col2.metric("Recovered", f"{df_filtered['Recovered'].sum():,}")
col3.metric("Deaths", f"{df_filtered['Deaths'].sum():,}")
col4.metric("Active", f"{df_filtered['Active'].sum():,}")

#graphs for COVID-19 trends and global spread
st.markdown("### COVID-19 Trends & Global Spread")
col1, col2, col3, col4 = st.columns(4)

with col1:
    fig_confirmed = px.bar(df_filtered, x="Date", y="Confirmed", title="Confirmed Cases Over Time", color_discrete_sequence=["blue"])
    st.plotly_chart(fig_confirmed, use_container_width=True)
    fig_map_confirmed = px.scatter_geo(df_country, locations="Country.Region", locationmode="country names", size="Confirmed", title="Confirmed Cases Worldwide", color_discrete_sequence=["blue"])
    st.plotly_chart(fig_map_confirmed, use_container_width=True)
    #fig_bar_confirmed = px.bar(df_continent, x ="Confirmed", y = "Continent", orientation = 'h', title = "Total Confirmed Cases by Continent", color = "Confirmed", color_continuous_scale = "Blues") 
    #st.plotly_chart(fig_bar_confirmed, use_container_width=True)

with col2:
    fig_recovered = px.bar(df_filtered, x="Date", y="Recovered", title="Recovered Cases Over Time", color_discrete_sequence=["green"])
    st.plotly_chart(fig_recovered, use_container_width=True)
    fig_map_recovered = px.scatter_geo(df_country, locations="Country.Region", locationmode="country names", size="Recovered", title="Recovered Cases Worldwide", color_discrete_sequence=["green"])
    st.plotly_chart(fig_map_recovered, use_container_width=True)


data = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]

# Auswahl der Datenebene
option = st.sidebar.selectbox("Select Data Scope:", ["Worldwide", "Continent", "Country"])


if option == "Worldwide":
    data = data.groupby("Date")[["Daily New Cases", "Daily New Deaths", "Daily New Recoveries", "Confirmed", "Deaths", "Recovered"]].sum().reset_index()
    scope_title = "Worldwide"
elif option == "Continent":
    available_continents = df["Continent"].dropna().unique()
    selected_continent = st.sidebar.selectbox("Select a Continent:", available_continents)
    data = data[data["Continent"] == selected_continent].groupby("Date")[["Daily New Cases", "Daily New Deaths", "Daily New Recoveries", "Confirmed", "Deaths", "Recovered"]].sum().reset_index()
    scope_title = selected_continent
elif option == "Country":
    selected_country = st.sidebar.selectbox("Select a Country:", df["Country.Region"].dropna().unique())
    data = data[data["Country.Region"] == selected_country].groupby("Date")[["Daily New Cases", "Daily New Deaths", "Daily New Recoveries", "Confirmed", "Deaths", "Recovered"]].sum().reset_index()
    scope_title = selected_country

# Line Charts anzeigen
line_chart(data, scope_title)


# --- COUNTRY COMPARISON ---
st.markdown("### Top 10 Affected Countries")
df_top_countries = df_country.sort_values(by="Confirmed", ascending=False).head(10)
top_countries_fig = px.bar(df_top_countries, x="Confirmed", y="Country.Region", title="Top 10 Countries by Confirmed Cases", color="Confirmed", orientation='h')
st.plotly_chart(top_countries_fig, use_container_width=True)


# --- CONTINENT COMPARISON ---
st.markdown("### Confirmed, Death Rates by Continent")
col1, col2 = st.columns(2)
connection = sqlite3.connect(db_path)
df_continents = get_continent_rates(connection, start_date, end_date).sort_values(by='Confirmed_rate_diff', ascending=True)
#df_continents.to_csv("continents_rates_filtered.csv", index=False)

with col1:
    fig1 = px.bar(df_continents, x="Confirmed_rate_diff", y="Continent", title="Continents' Confirmed Rates", text_auto=".2f", orientation='h')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(df_continents, x="Death_rate_diff", y="Continent", title="Continents' Deaths' Rates", text_auto=".2f", orientation='h')
    st.plotly_chart(fig2, use_container_width=True)

# Bar charts for Countries' Cases Rates by Continent
st.markdown("### Top 20 Countries by Cases Rates")
col1, col2, col3 = st.columns(3)
df_rates = get_cases_rates(connection, start_date, end_date, selected_continent).sort_values(by='Confirmed_Rate_diff', ascending=True).head(20)
countries_list = df_rates["Country"].tolist()
#df_rates.to_csv("cases_rates_filtered.csv", index=False)

with col1:
    fig1 = px.bar(df_rates, y="Country", x="Confirmed_Rate_diff", orientation="h", title="Confirmed Rate", text_auto=".2f")
    fig1.update_layout(title_x=0.5)
    fig1.update_yaxes(categoryorder="array", categoryarray=countries_list)
    fig1.update_xaxes(title_text="") 
    fig1.update_layout(yaxis_title="") 
    fig1.update_layout(xaxis=dict(range=[0, df_rates["Confirmed_Rate_diff"].max() * 1.1]))
    fig1.update_traces(hovertemplate="%{x:.2f}%")
    st.plotly_chart(fig1)

# Bar Chart: Deaths Rate (Keep same order as Confirmed Rate)
with col2:
    fig2 = px.bar(df_rates, y="Country", x="Deaths_Rate_diff", orientation="h", title="Deaths Rate", text_auto=".2f")
    fig2.update_layout(title_x=0.5)
    fig2.update_yaxes(categoryorder="array", categoryarray=countries_list)
    fig2.update_xaxes(title_text="") 
    fig2.update_layout(yaxis_title="") 
    fig2.update_layout(xaxis=dict(range=[0, df_rates["Deaths_Rate_diff"].max() * 1.1]))
    fig2.update_traces(hovertemplate="%{x:.2f}%")
    st.plotly_chart(fig2)

# Bar Chart: Recovered Rate (Keep same order as Confirmed Rate)
with col3:
    fig3 = px.bar(df_rates, y="Country", x="Recovered_Rate_diff", orientation="h", title="Recovered Rate", text_auto=".2f")
    fig3.update_layout(title_x=0.5)
    fig3.update_yaxes(categoryorder="array", categoryarray=countries_list)
    fig3.update_xaxes(title_text="")  
    fig3.update_layout(yaxis_title="")
    fig3.update_layout(xaxis=dict(range=[0, df_rates["Recovered_Rate_diff"].max() * 1.1])) 
    fig3.update_traces(hovertemplate="%{x:.2f}%")
    st.plotly_chart(fig3)


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    body, .stApp {
        background-color: #D3D3D3; /* Helles Grau für den Hauptbereich */
        color: #000000; /* Schwarzer Text */
        font-family: 'Montserrat', sans-serif; /* Neue Schriftart */
    }

    .stSidebar {
    background-color: #777777; /* Mittelgrau für die Sidebar */
    color: #FFFFFF;
    font-family: 'Montserrat', sans-serif;
    }

    .stSelectbox, .stDateInput, .stMetric, .stPlotlyChart {
        background-color: #F0F0F0; /* Noch helleres Grau für Elemente */
        color: #000000;
        border-radius: 10px;
        padding: 8px;
        font-family: 'Montserrat', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Montserrat', sans-serif;
        font-weight: 700; /* Dickere Überschriften */
    }

    </style>
    """,
    unsafe_allow_html=True
)

csv_path = r"../data/complete.csv"
database_path = r"../data/covid_database.db"

conn = sqlite3.connect(database_path)
cursor = conn.cursor()

query_population = f"""
SELECT "Country.Region", Population
FROM worldometer_data
"""

df_population = pd.read_sql(query_population, conn)
df_population.rename(columns={"Country.Region" : "Country"}, inplace=True)
conn.close()

df = pd.read_csv(csv_path)

df.rename(columns={"Country.Region": "Country"}, inplace=True) 
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

df_combined = pd.merge(df, df_population, on="Country", how="left")
df_combined["Susceptible"] = df_combined["Population"] - df_combined["Active"].fillna(0) - df_combined["Deaths"].fillna(0) - df_combined["Recovered"].fillna(0)
df_combined["mu"] = float("nan")
df_combined["gamma"] = 1 / 4.5
df_combined["beta"] = float("nan")
df_combined["alpha"] = float("nan")
df_combined["R0"] = float("nan")





with st.sidebar:
    st.title("This is the title of the sidebar")
    st.write("This is the content of the sidebar")


# create maps
from maps import continent_map, world_map
import datetime
updated_df = pd.read_csv("../data/complete.csv")

min_date = datetime.date(2020, 1, 22)
max_date = datetime.date(2020, 7, 22)

date = st.slider("Select a date:", min_value = min_date, max_value = max_date, value = min_date)
world_map(updated_df, date)


continent = st.selectbox(
    "Select a continent",
    {"Europe", "Asia", "Africa", "North America", "South America"}
)

continent_map(updated_df, continent, date, connection)


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


col1, col2 = st.columns([1,1], gap= "medium")
with col1: 
    if selected_country:
        try:
            df_combined = calculate_sir_parameters(selected_country, df_combined)
            country_params = df_combined[df_combined["Country"] == selected_country]

            st.subheader(f"Parameters for {selected_country}")
            st.write(f"**Adjustment Factor (α):** {country_params['alpha'].values[0]:.4f}")
            st.write(f"**Transmission Rate (β):** {country_params['beta'].values[0]:.4f}")
            st.write(f"**Recovery Rate (γ):** {country_params['gamma'].values[0]:.4f}")
            st.write(f"**Mortality Rate (μ):** {country_params['mu'].values[0]:.4f}")
        except Exception as e:
            st.error(f"Error calculating parameters for {selected_country}: {str(e)}")                                    
            st.error(f"Error calculating parameters for {selected_country}: {str(e)}")

with col2:
    st.subheader(f"R0 Over Time for {selected_country}")
    fig, ax = plt.subplots()
    ax.plot(df_combined["Date"], df_combined["R0"], marker='o', linestyle='-', color='b')
    ax.set_xlim(start_date, end_date)
    ax.set_xlabel("Date")
    ax.set_ylabel("R0")
    ax.set_title(f"R0 Over Time for {selected_country}")
    st.pyplot(fig)

    connection.close()                                          
