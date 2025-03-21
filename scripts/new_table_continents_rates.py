import sqlite3
import pandas as pd

# Define database path
db_path = "../data/covid_database.db"

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop the existing table (for testing purposes)
cursor.execute("DROP TABLE IF EXISTS continents_rates")

# Create the Aggregated_Cases_rates table and insert data
cursor.executescript("""
CREATE TABLE continents_rates (
    Date TEXT NOT NULL,
    Continent TEXT NOT NULL,
    ConfirmedPerPop REAL,
    DeathPerPop REAL,
    RecoveredPerPop REAL,
    PRIMARY KEY (Date, Continent)
);

INSERT INTO continents_rates (Date, Continent, ConfirmedPerPop, DeathPerPop, RecoveredPerPop)
WITH AggregatedData AS (
    SELECT 
        STRFTIME('%m/%d/%Y', Date) AS Date,  -- Format Date to "MM/DD/YYYY" (use as text)
        Continent,
        SUM(Confirmed) AS Total_Confirmed,
        SUM(Deaths) AS Total_Deaths,
        SUM(Recovered) AS Total_Recovered,
        SUM(Population) AS Total_Population
    FROM new_complete
    WHERE Date IS NOT NULL AND TRIM(Date) != ''  -- Ensure we only use valid dates
    GROUP BY Date, Continent
)
SELECT 
    Date,
    Continent,
    (Total_Confirmed * 1000000.0 / NULLIF(Total_Population, 0)) AS ConfirmedPerPop,
    (Total_Deaths * 1000000.0 / NULLIF(Total_Population, 0)) AS DeathPerPop,
    (Total_Recovered * 1000000.0 / NULLIF(Total_Population, 0)) AS RecoveredPerPop
FROM AggregatedData;
""")

# Commit the changes
conn.commit()
conn.close()