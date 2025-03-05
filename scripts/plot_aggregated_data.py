import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_aggregated_data(df, level):
    """
    Generates a side-by-side bar plot of aggregated COVID-19 data
    with a secondary Y-axis for Deaths as a line plot.
    """
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Selecting a few top countries/counties/continents to avoid clutter
    top_df = df.sort_values(by="Confirmed", ascending=False).head(10)

    x = np.arange(len(top_df[level]))  # X-axis positions for bars
    width = 0.2  # Bar width

    # Plot bars (side-by-side)
    ax1.bar(x - width, top_df["Confirmed"], color="blue", label="Confirmed Cases", width=width, alpha=0.8)
    ax1.bar(x, top_df["Recovered"], color="green", label="Recovered", width=width, alpha=0.8)
    ax1.bar(x + width, top_df["Active"], color="orange", label="Active Cases", width=width, alpha=0.8)

    # Label primary Y-axis
    ax1.set_xlabel(level)
    ax1.set_ylabel("Cases (Confirmed, Recovered, Active)", color="black")
    ax1.tick_params(axis="y", labelcolor="black")
    ax1.set_title(f"COVID-19 Data by {level} with Dual Y-Axis")

    # Create secondary Y-axis for Deaths
    ax2 = ax1.twinx()
    ax2.plot(x, top_df["Deaths"], color="red", linestyle="-", marker = "o", markersize = 3, linewidth=1, label="Deaths")
    ax2.set_ylabel("Deaths", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

    # Format x-axis
    ax1.set_xticks(x)
    ax1.set_xticklabels(top_df[level], rotation=45, ha="right")

    # Combine legends from both axes
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    # Grid for better readability
    ax1.grid(axis="y", linestyle="--", alpha=0.5)

    # Show the plot
    plt.show()

    print(f"Updated aggregated data for {level} displayed.")
