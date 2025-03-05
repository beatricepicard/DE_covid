import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdts
import numpy as np
import datetime as datetime
import sqlite3


#part1
#subexcerside 1.1.: graphical display
from graphical_display import date

df = pd.read_csv("../data/day_wise.csv")
df["Date"] = pd.to_datetime(df["Date"])

print(df.head())
date(df)

#part1
#subexcerside 1.2.: SIR model
from SIRmodel import estimate_parameters, update_SIR_model, plot_SIR

#find initial conditions
I_0 = df['Active'].iloc[0]
R_0 = df['Recovered'].iloc[0]
D_0 = df['Deaths'].iloc[0]
S_0 = 170000000
N = I_0 + R_0 + D_0 + S_0

days = len(df)
S, I, R, D = [S_0], [I_0], [R_0], [D_0]
alpha, beta, gamma, mu = [0.01], [0.3], [0.1], [0.02]
R0 = [3]

for t in range(1, days):
    beta_new, gamma_new, alpha_new, mu_new = estimate_parameters(t, S, I, R, D, alpha, beta, gamma, mu, N)
    beta.append(beta_new)
    gamma.append(gamma_new)
    alpha.append(alpha_new)
    mu.append(mu_new)

    S_new, I_new, R_new, D_new = update_SIR_model(S, I, R, D, alpha_new, beta_new, gamma_new, mu_new, N)
    S.append(S_new)
    I.append(I_new)
    R.append(R_new)
    D.append(D_new)
    R0.append(beta_new / gamma_new if gamma_new > 0 else 0)

updated_df = pd.DataFrame({'Day': range(days), 'Susceptible': S, 'Infected': I, 'Recovered': R, 'Died': D})
plot_SIR(updated_df, R0, days)

# Connection to the database
connection = sqlite3.connect("../data/covid_database.db")
cursor = connection.cursor()

from aufgabe3melanie import data, death_rate_by_continent, plot_death_rate, top_us_counties

#part3.5: Death rate by continent
path = r"../data/covid_database.db"
print("Calculating death rate by continent...")
death_rate_df = death_rate_by_continent(path)
print(death_rate_df)
plot_death_rate(death_rate_df)

#part 3.6: top 5 US counties with most deaths and most recorded cases
print("Finiding top 5 US counties with most deaths and most recorded cases...")
top5_deaths, top5_cases = top_us_counties(path)
print("Top 5 US counties with most deaths:")
print(top5_deaths[['County', 'State', 'total_deaths']])
print("Top 5 US counties with most recorded cases:")   
print(top5_cases[['County', 'State', 'total_cases']])   


connection = sqlite3.connect("../data/covid_database.db")
cursor = connection.cursor()

# Add complete.csv to the database
df = pd.read_csv("../data/complete.csv")

tablename = "complete"
df.to_sql(tablename, connection, if_exists="replace")

# print(df.duplicated())

cleaned_df = df.drop_duplicates()
cleaned_df.sample()

# print(cleaned_df)
# print(sum(cleaned_df.duplicated()))

# Part 4 bullet 4
from groupings import group_by_country, group_by_state
group_by_country(connection)
group_by_state(connection)

#Country Aggregation:
from aggregation import aggregation

df_country, df_county, df_continent = aggregation(cleaned_df, connection)
print("Country Aggregation:", df_country, "County Aggregation:", df_county, "Continent Aggregation:", df_continent)


#extract COVID-19 data per country
from country_summary import country_summary
country_name = input("Enter the country name: ")
country_stats = country_summary(country_name, connection)
print(country_stats)

from plot_country import plot_country_statistics
from plot_aggregated_data import plot_aggregated_data

#plot country statistics
plot_country_statistics(country_name, connection)
plot_aggregated_data(df_country, "Country.Region")


connection.close()

