import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import plotly.express as px
from aggregation import aggregation
from country_summary import country_summary
from get_countries import get_countries
from line_chart import line_chart


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
   
 
    
 
import seaborn as sns

def calculate_sir_parameters(country_name, df):
    country_df = df[df["Country"] == country_name].copy()
    if country_df.empty:
        raise ValueError(f"No data found for {country_name}")
    
    country_df.sort_values("Date", inplace=True)

    country_df["DeltaS"] = country_df["Susceptible"].diff()
    country_df["DeltaI"] = country_df["Active"].diff()
    country_df["DeltaR"] = country_df["Recovered"].diff()
    country_df["DeltaD"] = country_df["Deaths"].diff()

    country_df["alpha"] = (-country_df["DeltaR"] + country_df["gamma"] * country_df["Recovered"]) / country_df["Recovered"]
    country_df["beta"] = (-country_df["DeltaS"] + country_df["alpha"] * country_df["Recovered"]) * country_df["Population"] / (country_df["Susceptible"] * country_df["Active"])
    country_df["mu"] = country_df["DeltaD"] / country_df["Active"]
    country_df["R0"] = country_df["beta"] / country_df["gamma"]

    df.loc[df["Country"] == country_name, ["mu", "beta", "alpha", "R0"]] = country_df[["mu", "beta", "alpha", "R0"]]

    return df

csv_path = r"..\data\complete.csv"
database_path = r"..\data\covid_database.db"

conn = sqlite3.connect(database_path)
cursor = conn.cursor()

query_population = f"""
SELECT "Country.Region", Population
FROM worldometer_data
"""

df_population = pd.read_sql(query_population, conn)
df_population.rename(columns={"Country.Region" : "Country"}, inplace=True)
conn.close()

df_csv = pd.read_csv(csv_path)

df_csv.rename(columns={"Country.Region": "Country"}, inplace=True) 
df_csv["Date"] = pd.to_datetime(df_csv["Date"], errors='coerce')

df_combined = pd.merge(df_csv, df_population, on="Country", how="left")
df_combined["Susceptible"] = df_combined["Population"] - df_combined["Active"].fillna(0) - df_combined["Deaths"].fillna(0) - df_combined["Recovered"].fillna(0)
df_combined["mu"] = float("nan")
df_combined["gamma"] = 1 / 4.5
df_combined["beta"] = float("nan")
df_combined["alpha"] = float("nan")
df_combined["R0"] = float("nan")

def calculate_sir_parameters(country_name, df):
   country_df = df[df["Country"] == country_name].copy()
   if country_df.empty:
       raise ValueError(f"No data found for {country_name}")
   
   country_df.sort_values("Date", inplace=True)
   country_df["DeltaS"] = country_df["Susceptible"].diff()
   country_df["DeltaI"] = country_df["Active"].diff()
   country_df["DeltaR"] = country_df["Recovered"].diff()
   country_df["DeltaD"] = country_df["Deaths"].diff()

   country_df["alpha"] = (-country_df["DeltaR"] + country_df["gamma"] * country_df["Recovered"]) / country_df["Recovered"]
   country_df["beta"] = (-country_df["DeltaS"] + country_df["alpha"] * country_df["Recovered"])* country_df["Population"] / (country_df["Susceptible"] * country_df["Active"])
   country_df["mu"] = country_df["DeltaD"] / country_df["Active"]
   country_df["R0"] = country_df["beta"] / country_df["gamma"]
   
   avg_alpha = country_df["alpha"].mean()
   avg_beta = country_df["beta"].mean()
   avg_mu = country_df["mu"].mean()
   
   df.loc[df["Country"] == country_name, "mu"] = avg_mu
   df.loc[df["Country"] == country_name, "beta"] = avg_beta
   df.loc[df["Country"] == country_name, "alpha"] = avg_alpha
   df.loc[df["Country"] == country_name, "R0"] = country_df["R0"]

   return df


connection.close()

with st.sidebar:
    st.title("This is the title of the sidebar")
    st.write("This is the content of the sidebar")

# create maps
from maps import continent_map, world_map

world_map(conn)

continent = st.selectbox(
    "Select a continent",
    {"Europe", "Asia", "Africa", "North America", "South America"}
)

continent_map(conn, continent)


st.header("The SIR Model")
col1, col2 = st.columns([1,1], gap= "medium")
with col1: 
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

with col2:
    selected_country = st.selectbox("Select a country:", df_combined["Country"].unique())

    if selected_country:
        try:
            df_combined = calculate_sir_parameters(selected_country, df_combined)
            country_params = df_combined[df_combined["Country"] == selected_country]

            st.subheader(f"Parameters for {selected_country}")
            st.write(f"**Adjustment Factor (α):** {country_params['alpha'].values[0]:.4f}")
            st.write(f"**Transmission Rate (β):** {country_params['beta'].values[0]:.4f}")
            st.write(f"**Recovery Rate (γ):** {country_params['gamma'].values[0]:.4f}")
            st.write(f"**Mortality Rate (μ):** {country_params['mu'].values[0]:.4f}")

            st.subheader(f"R0 Over Time for {selected_country}")
            fig, ax = plt.subplots()
            ax.plot(df_combined["Date"], df_combined["R0"], marker='o', linestyle='-', color='b')
            ax.set_xlabel("Date")
            ax.set_ylabel("R0")
            ax.set_title(f"R0 Over Time for {selected_country}")
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error calculating parameters for {selected_country}: {str(e)}")                                    

connection.close()