import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as datetime

def date(df):
    date1 = input("When should the graph start? (yyyy-mm-dd)")
    date2 = input("When should the graph end? (yyyy-mm-dd)")
    date1 = pd.to_datetime(date1)
    date2 = pd.to_datetime(date2)
    graph(df, date1, date2)


def graph(df, date1, date2):
    new_df = df[(df['Date'] >= date1) & (df['Date'] <= date2 )]

    fig = plt.figure(figsize=(12,8))

    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2,2,2)
    ax3 = fig.add_subplot(2, 2, 3)

    new_df["New cases"].plot.line(ax = ax1, title = "New cases", xlabel = "Date", ylabel = "amount of people")
    new_df["Deaths"].plot.line(ax = ax2, title = "Deaths", xlabel = "Date", ylabel = "amount of people")
    new_df["Recovered"].plot.line(ax = ax3, title = "Recovered", xlabel = "Date", ylabel = "ambount of people")

    ax1.set_xticklabels(new_df['Date'], rotation=90)  
    ax2.set_xticklabels(new_df['Date'], rotation=90)  
    ax3.set_xticklabels(new_df['Date'], rotation=90)  

    plt.tight_layout()
    plt.show()