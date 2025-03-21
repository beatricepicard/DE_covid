import pandas as pd

from get_continent import get_continent

def data(df):
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
    
    return df