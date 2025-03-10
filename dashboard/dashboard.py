
import streamlit as st
import pandas as pd
import sqlite3

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

csv_path = r"C:\Users\irini\OneDrive\Desktop\uptodate3\DE_Covid\data\complete.csv"
database_path = r"C:\Users\irini\OneDrive\Desktop\uptodate3\DE_Covid\data\covid_database.db"

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

def calculate_sir_parameters(country_name, df):
   country_df = df[df["Country"] == country_name].copy()
   if country_df.empty:
       raise ValueError(f"No data found for {country_name}")
   
   country_df.sort_values("Date", inplace=True)
   country_df["DeltaS"] = country_df["Susceptible"].diff()
   country_df["DeltaI"] = country_df["Active"].diff()
   country_df["DeltaR"] = country_df["Recovered"].diff()
   country_df["DeltaD"] = country_df["Deaths"].diff()
   
   avg_alpha = ((-country_df["DeltaR"] + country_df["gamma"] * country_df["Recovered"]) / country_df["Recovered"]).mean()
   avg_beta = (((-country_df["DeltaS"] + avg_alpha * country_df["Recovered"]) * country_df["Population"]) / (country_df["Susceptible"] * country_df["Active"])).mean()
   avg_mu = ((country_df["DeltaD"] / country_df["Active"])).mean()
   
   df.loc[df["Country"] == country_name, "mu"] = avg_mu.mean()
   df.loc[df["Country"] == country_name, "beta"] = avg_beta.mean()
   df.loc[df["Country"] == country_name, "alpha"] = avg_alpha.mean()

   return df



st.set_page_config(page_title = "Summary of Covid-Data", layout = "wide", initial_sidebar_state = "expanded")

st.title("Summary of Covid-Data")

with st.sidebar:
    st.title("This is the title of the sidebar")
    st.write("This is the content of the sidebar")

st.header("The SIR Model")
col1, col2 = st.columns([2,1])
with col1: 
    st.text("The spread of epidemics is often described using the SIR model, which tracks individuals in a population as Susceptible (S), Infected (I), or Recovered (R). In this case, an additional category is included: Deceased (D).")
    st.text("Each day, individuals can either remain in their current state or transition to an adjacent state. For example, an infected person can recover, succumb to the disease, or stay infected, while a deceased individual remains in that state permanently.")
    st.text("The daily changes in the population are governed by the following equations:")
    st.latex(r"\Delta S(t) = \alpha R(t) - \beta S(t) \frac{I(t)}{N}")
    st.latex(r"\Delta I(t) = \beta S(t) \frac{I(t)}{N} - \mu I(t) - \gamma I(t)")
    st.latex(r"\Delta R(t) = \gamma I(t) - \alpha R(t)")
    st.latex(r"\Delta D(t) = \mu I(t)")
    

with col2:
    st.text("By estimating the parameters for each country, we can fill in missing values, leading to better predictive performance.")
    selected_country = st.selectbox("Select a country:", df_combined["Country"].unique())

    if selected_country:
        try:
            df_combined = calculate_sir_parameters(selected_country, df_combined)
            country_params = df_combined[df_combined["Country"] == selected_country].iloc[-1]

            st.subheader(f"Parameters for {selected_country}")
            st.write(f"**Adjustment Factor (α):** {country_params['alpha']:.4f}")
            st.write(f"**Transmission Rate (β):** {country_params['beta']:.4f}")
            st.write(f"**Recovery Rate (γ):** {country_params['gamma']:.4f}")
            st.write(f"**Mortality Rate (μ):** {country_params['mu']:.4f}")

        except Exception as e:
            st.error(f"Error calculating parameters for {selected_country}: {str(e)}")                                    
