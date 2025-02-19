import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import numpy as np
import datetime as datetime

def date(df):
    date1 = input("When should the graph start? (YYYY-MM-DD) ")
    date2 = input("When should the graph end? (YYYY-MM-DD) ")
    date1 = pd.to_datetime(date1)
    date2 = pd.to_datetime(date2)
    graph(df, date1, date2)


def graph(df, date1, date2):
    new_df = df[(df['Date'] >= date1) & (df['Date'] <= date2 )]

    fig, (ax1, ax2, ax3) = plt.subplots(ncols = 3, figsize = (16,5))

    new_df.plot.line(x = "Date", y = "New cases", ax = ax1, title = "New cases", xlabel = "Date", ylabel = "amount of people")
    new_df.plot.line(x = "Date", y = "Deaths", ax = ax2, title = "Deaths", xlabel = "Date", ylabel = "amount of people")
    new_df.plot.line(x = "Date", y = "Recovered", ax = ax3, title = "Recovered", xlabel = "Date", ylabel = "ambount of people")

    # plt.xticks(pd.date_range(date1, date2, periods=10)) 

    # with everyone's permission we can delete this. This actually messes with the graph.
    # ax1.set_xticklabels(new_df['Date'], rotation=90)  
    # ax2.set_xticklabels(new_df['Date'], rotation=90)  
    # ax3.set_xticklabels(new_df['Date'], rotation=90)  

    plt.tight_layout()
    plt.show()