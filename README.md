# COVID-19 Dashboard

This project presents an interactive dashboard to explore the spread of COVID-19 globally. It was developed as part of the Data Engineering course at Vrije Universiteit Amsterdam.

---

## Project Overview
The COVID-19 Dashboard is a complete data analysis and visualization tool for exploring the progression of the pandemic. It includes:

- Analysis and visualization of daily COVID-19 case dynamics across countries and continents,
- Parameter estimation for the SIR epidemiological model,
- Integration and querying of a SQLite database,
- Choropleth maps and interactive charts via Plotly and Streamlit,
- A responsive dashboard with date and regional filters.

---

## Prerequisites

Make sure you have **Python 3.8 or higher** installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

Then, open your terminal or command prompt and install the required libraries:

```bash
pip install streamlit pandas matplotlib plotly numpy
```

### Libraries Used

- **streamlit** - to create the interactive web dashboard 
- **numpy** - for numerical operations
- **matplotlib** - for data visualization
- **pandas** - for data manipulation and analysis
- **plotly** - for interactive charts and maps
- **sqlite3** - for connecting to the SQLite database (built-in)
- **datetime** - to handle and format date inputs for filtering (built-in)

> **Note:** `datetime` and `sqlite3` are included with Python, so no need to install them.


---

## How to Run the dashboard

### Step 1: Clone this Repository

```bash
   git clone https://github.com/beatricepicard/DE_covid.git
   cd DE_Covid
   cd dashboard
```

### Step 2: Run the dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open in your default web browser. You can now explore global and regional COVID-19 trends, compare countries and view simulations of the SIR model. 

---

## Repository Structure

The repository includes the following files and folders:

📂 **dashboard/** - Contains all files to run the dashboard.
- `dashboard.py`: The entry point that ties all components together and runs the app.
- `cases_rates.py`: Calculates per capita case rates by country within a continent.
- `continent_rate_comparison.py`: Compares per capita statistics across continents.
- `country_data.py`: Displays visualizations and comparisons for selected countries.
- `continent_data.py`: Plots continent-level time trends and active case maps.
- `global_data.py`: Displays global stats and map of worldwide active cases.
- `sir_model.py`: Implements the SIR model with death states and computes R₀.
- `maps.py`: Draws choropleth maps of the world or continents using Plotly.
- `line_chart.py`: Generates time-series plots for new and total case metrics.
- `date.py`: Streamlit-based date selector for filtering data.
- `organizing_data.py`: Prepares raw data by calculating daily changes.
- `design.py`: Adds custom CSS styles for a clean dashboard look.
- `get_countries.py`: Helper to extract list of countries from the database.
- `requirements.txt`: Indicates package dependencies for dashboard deployment.


📂 **data/** — Contains all datasets used for the project.
- `covid_database.db`: SQLite database with cleaned and structured COVID-19 data.
- `complete.csv`: Raw country-level time series data (imported into the DB).
- `day_wise.csv`: Global daily summaries of the COVID-19 pandemic.

📄 **README.md** — This file! Contains documentation and setup instructions.

📂 **scripts/** - Files created during the course for practice purposes *(not required for the dashboard)*.
> **Note:** These scripts were made for testing and learning during the Data Engineering course. They are **not used** in the Streamlit dashboard.  
> **Note:** You can run them by calling `main.py`.

- `main.py`: Runs a combination of tasks: shows charts, runs a SIR simulation, compares death rates, and queries the database.
- `aggregation.py`: Aggregates COVID stats by country, county, and continent.
- `aufgabe3melanie.py`: Estimates death rates by continent and finds top 5 US counties for deaths and cases.
- `cases_by_country_pie_chart.py`: Creates a pie chart of active, recovered, and death cases for a specific country.
- `Cases_by_country_time_series.py`: Visualizes COVID case rates over time as a percentage of population (light + dark themes).
- `country_summary.py`: Returns a dictionary with key figures (total cases, deaths, etc.) for a selected country.
- `europe_maps.py`: Generates choropleth maps for Europe and the world showing active cases per population.
- `fill_in_nans.py`: Fills missing data in the dataset using estimated SIR parameters and updates the CSV.
- `generate_new_complete.py`: Generates a new, cleaned and complete version of the dataset using grouping and model estimation.
- `graphical_display.py`: Creates basic time series charts of new cases, deaths, and recoveries between user-defined dates.
- `groupings.py`: Groups and summarizes data by country or US state.
- `insertiong_lacking_population.py`: Inserts missing population data directly into the SQLite database.
- `new_table_continents_rates.py`: Creates the `continents_rates` table with normalized COVID stats (per 1M pop).
- `parametersandr0.py`: Calculates and plots the evolution of SIR parameters and R₀ for a selected country.
- `part3bullet2.py`: Estimates SIR model parameters directly using new/deaths/recovered per day.
- `plot_aggregated_data.py`: Bar plot comparing confirmed, recovered, active, and deaths across top 10 entities.
- `plot_country.py`: Plots total COVID stats over time for a single selected country.
- `SIRmodel.py`: Contains helper functions for estimating and simulating SIR model behavior.
- `top_populated_countries_covid_rates.py`: Compares active, death, and recovery rates across the 20 most populated countries.


## Project Link
GitHub Repository: [https://github.com/beatricepicard/DE_covid](https://github.com/beatricepicard/DE_covid)

---

## Project Team
This project was developed by:

- **Nataliia Krysanova**
- **Béatrice Picard**
- **Eirini Papathanasiadi**
- **Melanie Ackermann**

---
