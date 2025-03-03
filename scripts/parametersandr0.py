import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

csv_path = r"C:\Users\irini\OneDrive\Desktop\uptodate2\DE_Covid\complete.csv"
database_path = r"C:\Users\irini\OneDrive\Desktop\uptodate2\DE_Covid\data\covid_database.db"
df_complete = pd.read_csv(csv_path)

df_complete.rename(columns={"Country.Region": "Country"}, inplace=True)

df_complete["Day"] = df_complete.groupby("Country").cumcount() + 1

conn = sqlite3.connect(database_path)

df_worldometer = pd.read_sql("SELECT * FROM worldometer_data", conn)

df_worldometer.rename(columns={"Country.Region": "Country"}, inplace=True)

df_combined = pd.merge(df_complete, df_worldometer, on="Country", how="left")

required_columns = ["Active", "Deaths", "Recovered", "Population"]
missing_columns = [col for col in required_columns if col not in df_combined.columns]
if missing_columns:
    raise KeyError(f"Missing columns in merged dataset: {missing_columns}")


df_combined.dropna(subset=required_columns, inplace=True)

df_combined["Susceptible"] = df_combined["Population"] - df_combined["Active"] - df_combined["Deaths"] - df_combined["Recovered"]
df_combined["mu"] = float("nan")
df_combined["gamma"] = 1 / 4.5  
df_combined["beta"] = float("nan")
df_combined["alpha"] = float("nan")
df_combined["R0"] = float("nan")

def calculate_sir_parameters(country_name, df):
    country_df = df[df["Country"] == country_name].copy()
    if country_df.empty:
        raise ValueError(f"No data found for {country_name}")
    
    country_df["DeltaS"] = country_df["Susceptible"].diff()
    country_df["DeltaI"] = country_df["Active"].diff()
    country_df["DeltaR"] = country_df["Recovered"].diff()
    country_df["DeltaD"] = country_df["Deaths"].diff()
    
    country_df["alpha"] = (country_df["DeltaR"] + country_df["gamma"] * country_df["Recovered"]) / country_df["Recovered"]
    country_df["beta"] = (-country_df["DeltaS"] + country_df["alpha"] * country_df["Recovered"]) / (country_df["Susceptible"] * (country_df["Active"] / country_df["Population"]))
    country_df["mu"] = country_df["DeltaD"] / country_df["Active"]
    country_df["R0"] = country_df["beta"] / country_df["gamma"]
    
    df.loc[df["Country"] == country_name, ["mu", "beta", "alpha", "R0"]] = country_df[["mu", "beta", "alpha", "R0"]]

    return df


selected_country = "Greece"
parameters = calculate_sir_parameters(selected_country, df_combined)

def plot_sir_parameters(country_name, df):
    country_df = df[df["Country"] == country_name]
    if country_df.empty:
        raise ValueError(f"No data found for {country_name}")
    
    plt.figure(figsize=(10, 6))
    plt.plot(country_df["Day"], country_df["mu"], label="mu (Mortality Rate)", marker='o')
    plt.plot(country_df["Day"], country_df["gamma"], label="gamma (Recovery Rate)", marker='s')
    plt.plot(country_df["Day"], country_df["beta"], label="beta (Transmission Rate)", marker='^')
    plt.plot(country_df["Day"], country_df["alpha"], label="alpha (Adjustment Factor)", marker='x')
    plt.xlabel("Day")
    plt.ylabel("Parameter Value")
    plt.title(f"SIR Model Parameters Over Time for {country_name}")
    plt.legend()
    plt.grid()
    plt.show()

plot_sir_parameters(selected_country, calculate_sir_parameters(selected_country, df_combined))

def plot_r0_trajectory(df, country_name):
   country_df = df[df["Country"] == country_name].copy()
   plt.figure(figsize=(10,6))
   plt.plot(country_df["Day"], country_df["R0"], label = "R0 value", marker = 'o', color = 'b')
   plt.xlabel("Day")
   plt.ylabel("R0 Value")
   plt.title(f"R0 Trajectory Over Time for {country_name}")
   plt.legend()
   plt.grid()
   plt.show()
    

plot_r0_trajectory(calculate_sir_parameters(selected_country, df_combined), selected_country)

