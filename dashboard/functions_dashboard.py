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