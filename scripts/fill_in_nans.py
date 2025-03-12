import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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

def calculate_sir_parameters(country_name, df):
   country_df = df[df["Country"] == country_name].copy()
   if country_df.empty:
       raise ValueError(f"No data found for {country_name}")
   
   country_df.sort_values("Date", inplace=True)
   country_df["DeltaS"] = country_df["Susceptible"].diff()
   country_df["DeltaI"] = country_df["Active"].diff()
   country_df["DeltaR"] = country_df["Recovered"].diff()
   country_df["DeltaD"] = country_df["Deaths"].diff()
   
   avg_alpha = (-country_df["DeltaR"] + country_df["gamma"] * country_df["Recovered"]) / country_df["Recovered"].mean()
   avg_beta = ((-country_df["DeltaS"] + avg_alpha * country_df["Recovered"]) * country_df["Population"]) / (country_df["Susceptible"] * country_df["Active"]).mean()
   avg_mu = (country_df["DeltaD"] / country_df["Active"]).mean()
   
   df.loc[df["Country"] == country_name, "mu"] = avg_mu.mean()
   df.loc[df["Country"] == country_name, "beta"] = avg_beta.mean()
   df.loc[df["Country"] == country_name, "alpha"] = avg_alpha.mean()

   return df


def fill_nan_values(country, df_combined, df_clean):
    df_country = df_combined[df_combined['Country'] == country].copy()
    df_clean_country = df_clean[df_clean['Country'] == country].copy()
        
    alpha = df_clean_country['alpha'].values[0]
    beta = df_clean_country['beta'].values[0]
    gamma = df_clean_country['gamma'].values[0]
    mu = df_clean_country['mu'].values[0]
        
    for col in ['Active', 'Recovered', 'Deaths']:
        first_valid_idx = df_country[col].first_valid_index()
        if first_valid_idx is not None:
            df_country.loc[:first_valid_idx - 1, col] = 0
        
    N = df_country['Population'].values[0] 
    for i in range(1, len(df_country)):
        if pd.isna(df_country.loc[df_country.index[i], 'Active']):
            S_prev = df_country.loc[df_country.index[i-1], 'Susceptible']
            I_prev = df_country.loc[df_country.index[i-1], 'Active']
            R_prev = df_country.loc[df_country.index[i-1], 'Recovered']
            D_prev = df_country.loc[df_country.index[i-1], 'Deaths']
            dS = alpha * R_prev - beta * S_prev * I_prev / N
            dI = beta * S_prev * I_prev / N - mu * I_prev - gamma * I_prev
            dR = gamma * I_prev - alpha * R_prev
            dD = mu * I_prev
            df_country.loc[df_country.index[i], 'Susceptible'] = S_prev + dS
            df_country.loc[df_country.index[i], 'Active'] = I_prev + dI
            df_country.loc[df_country.index[i], 'Recovered'] = R_prev + dR
            df_country.loc[df_country.index[i], 'Deaths'] = D_prev + dD
        
    df_combined.update(df_country)
    return df_combined


def fill_nans_for_all(df_combined, df_clean):
    countries = df_combined['Country'].unique()
    for country in countries:
        df_combined = fill_nan_values(country, df_combined, df_clean)
    return df_combined


def plot_covid_data(df_filled):
    countries = df_filled['Country'].unique()
    for country in countries:
        df_country = df_filled[df_filled['Country'] == country]
        plt.figure(figsize=(10, 5))
        plt.plot(df_country['Date'], df_country['Active'], label='Active Cases', color='blue')
        plt.plot(df_country['Date'], df_country['Recovered'], label='Recovered Cases', color='green')
        plt.plot(df_country['Date'], df_country['Deaths'], label='Deaths', color='red')
        plt.xlabel('Date')
        plt.ylabel('Number of Cases')
        plt.title(f'COVID-19 Cases in {country}')
        plt.legend()
        plt.xticks(rotation=45)
        plt.show()


countries = df_combined['Country'].unique()

for country in countries:
    try:
        df_clean = calculate_sir_parameters(country, df_clean)
    except Exception as e:
        print(f"Not enough data for {country}. Skipping. Error: {e}")
        continue
    df_combined = fill_nan_values(country, df_combined, df_clean)




