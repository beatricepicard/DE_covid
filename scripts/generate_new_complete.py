import sqlite3
import pandas as pd
import numpy as np


# Function that calculates the SIR parameters in order to fill in the missing values in the data frame
def calculate_sir_parameters(country_name, df):
   country_df = df[df["Country"] == country_name].copy()
   if country_df.empty:
       raise ValueError(f"No data found for {country_name}")
   
   country_df.sort_values("Date", inplace=True)
   country_df["DeltaS"] = country_df["Susceptible"].diff()
   country_df["DeltaI"] = country_df["Active"].diff()
   country_df["DeltaR"] = country_df["Recovered"].diff()
   country_df["DeltaD"] = country_df["Deaths"].diff()

   recovered_mean = country_df["Recovered"].mean()
   if recovered_mean == 0 or np.isnan(recovered_mean):
        recovered_mean = 1e-6 
   
   avg_alpha = (-country_df["DeltaR"] + country_df["gamma"] * country_df["Recovered"]) / recovered_mean

   if country_df["Deaths"].isna().all():
        country_df["Deaths"] =0 
        avg_mu = 0
   else:
        active_mean = country_df["Active"].mean()
        if active_mean == 0 or np.isnan(active_mean):
            active_mean = 1e-6  
        avg_mu = (country_df["DeltaD"] / country_df["Active"]).mean()

   country_df["Population"] = country_df["Population"].replace(0, 1e6).fillna(1e6)
   country_df["Susceptible"] = country_df["Susceptible"].replace(0, 1e-6).fillna(1e-6)
   country_df["Active"] = country_df["Active"].replace(0, 1e-6).fillna(1e-6)

   avg_beta = ((-country_df["DeltaS"] + avg_alpha * country_df["Recovered"]) * country_df["Population"]) / (country_df["Susceptible"] * country_df["Active"]).mean()

   
   df.loc[df["Country"] == country_name, "mu"] = avg_mu.mean()
   df.loc[df["Country"] == country_name, "beta"] = avg_beta.mean()
   df.loc[df["Country"] == country_name, "alpha"] = avg_alpha.mean()

   return df


# Function that fills in the missing values in order to receive a complete dataframe
def fill_nan_values(country, df_combined, df_clean):
    df_country = df_combined[df_combined['Country'] == country].copy()
    df_clean_country = df_clean[df_clean['Country'] == country].copy()
        
    alpha = df_clean_country['alpha'].values[0]
    beta = df_clean_country['beta'].values[0]
    gamma = df_clean_country['gamma'].values[0]
    mu = df_clean_country['mu'].values[0]

    if df_country['Deaths'].isna().all():
        df_country['Deaths'] = 0
        mu = 0
        
    for col in ['Active', 'Recovered', 'Deaths']:
        first_valid_idx = df_country[col].first_valid_index()
        if first_valid_idx is not None:
            df_country.loc[:first_valid_idx - 1, col] = 0

    if df_country['Population'].isna().any() or (df_country['Population'] <= 0).any():
        print(f"Warning: Invalid population for {country}. Setting default.")
        df_country['Population'].fillna(1e6, inplace=True)
        
    N = df_country['Population'].values[0] 
    if N == 0:
        N = 1e6  

    for i in range(1, len(df_country)):
        if pd.isna(df_country.loc[df_country.index[i], 'Active']):
            S_prev = df_country.loc[df_country.index[i-1], 'Susceptible']
            I_prev = df_country.loc[df_country.index[i-1], 'Active']
            R_prev = df_country.loc[df_country.index[i-1], 'Recovered']
            D_prev = df_country.loc[df_country.index[i-1], 'Deaths']
            S_prev = max(S_prev, 1e-6)
            I_prev = max(I_prev, 1e-6)

            dS = alpha * R_prev - beta * S_prev * I_prev / N
            dI = beta * S_prev * I_prev / N - mu * I_prev - gamma * I_prev
            dR = gamma * I_prev - alpha * R_prev
            dD = mu * I_prev

            dS = np.clip(dS, -1e6, 1e6)
            dI = np.clip(dI, -1e6, 1e6)
            dR = np.clip(dR, -1e6, 1e6)
            dD = np.clip(dD, -1e6, 1e6)

            # make sure death rate is not negative
            dD = max(0, dD)

            df_country.loc[df_country.index[i], 'Susceptible'] = S_prev + dS
            df_country.loc[df_country.index[i], 'Active'] = I_prev + dI
            df_country.loc[df_country.index[i], 'Recovered'] = R_prev + dR
            df_country.loc[df_country.index[i], 'Deaths'] = D_prev + dD
        
    df_combined.update(df_country)
    return df_combined

# Function that uses groupby to add up values for countries with several territories, such as France or the UK
def aggregate_territories(df):
    df_clean = df.drop(columns=['Province.State', 'Lat', 'Long', 'WHO.Region'])
    df_aggregated = df.groupby(['Country', 'Date']).agg({
        'Confirmed': 'sum',
        'Deaths': 'sum',
        'Recovered': 'sum',
        'Active': 'sum'
    }).reset_index()
    return df_aggregated

# add column with active cases per population
def active_cases(df):
    df["ActivePerPop"] = df["Active"] / df["Population"]
    df["ConfirmedPerPop"] = df["Confirmed"] / df["Population"]
    df["DeathsPerPop"] = df["Deaths"] / df["Population"]
    df["RecoveredPerPop"] = df["Recovered"] / df["Population"]
    return df


# connection to the database
connection = sqlite3.connect("../data/covid_database.db")
cursor = connection.cursor()

# load dataframe with population and continent for each country
query_pop_cont = f"SELECT \"Country.Region\", Population, Continent FROM worldometer_data"
df_pop_cont = pd.read_sql(query_pop_cont, connection)
df_pop_cont.rename(columns={"Country.Region" : "Country"}, inplace=True)

# load dataframe with complete data for the full timeframe
query_complete = f"SELECT * FROM complete"
df_complete = pd.read_sql(query_complete, connection)
df_complete.rename(columns={"Country.Region": "Country"}, inplace=True)

# transform entries into propper format
df_complete["Date"] = pd.to_datetime(df_complete["Date"], errors='coerce')
df_complete["Country"] = df_complete["Country"].str.replace(r"\*", "", regex=True)

# Use groupby operations to sum case numbers for countries with several territories
df_aggregated = aggregate_territories(df_complete)

# create a combined dataframe which adds populations and continents to the aggregated dataframe
df_combined = pd.merge(df_aggregated, df_pop_cont, on="Country", how="left")

# clean and add missing values to this new dataframe
df_combined.loc[(df_combined["Country"] == "Brunei") & (df_combined["Population"].isna()), "Population"] = 442000
df_combined.loc[(df_combined["Country"] == "Brunei") & (df_combined["Continent"].isna()), "Continent"] = "Asia"
df_clean = df_combined.dropna(subset=["Active", "Deaths", "Recovered", "Population"]).copy()

df_clean["Susceptible"] = df_clean["Population"] - df_clean["Active"].fillna(0) - df_clean["Deaths"].fillna(0) - df_clean["Recovered"].fillna(0)
df_clean["mu"] = float("nan")
df_clean["gamma"] = 1 / 4.5
df_clean["beta"] = float("nan")
df_clean["alpha"] = float("nan")

df_combined["Susceptible"] = df_combined["Population"] - df_combined["Active"].fillna(0) - df_combined["Deaths"].fillna(0) - df_combined["Recovered"].fillna(0)
df_combined["mu"] = float("nan")
df_combined["gamma"] = 1 / 4.5
df_combined["beta"] = float("nan")
df_combined["alpha"] = float("nan")

# calling the functions to fill in the missing values
countries = df_combined['Country'].unique()
for country in countries:
    try:
        df_clean = calculate_sir_parameters(country, df_clean)
    except Exception as e:
        # print(f"Not enough data for {country}. Skipping. Error: {e}")
        continue
    df_combined = fill_nan_values(country, df_combined, df_clean)

df_full = active_cases(df_combined)
df_full['Date'] = pd.to_datetime(df_full['Date']).dt.date
print(df_full)

# Adding the new_complete table to the database in order to use it for further computations and visualizations
df_full.to_sql('new_complete', connection, if_exists='replace', index=False)

connection.commit()
connection.close()
