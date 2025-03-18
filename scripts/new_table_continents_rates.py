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
    Confirmed_rate REAL,
    Death_rate REAL,
    PRIMARY KEY (Date, Continent)
);

INSERT OR REPLACE INTO continents_rates (Date, Continent, Confirmed_rate, Death_rate)
WITH AggregatedData AS (
    SELECT 
        c.Date,
        w.Continent,
        SUM(c.Confirmed) AS Total_Confirmed,
        SUM(c.Deaths) AS Total_Deaths,
        SUM(DISTINCT w.Population) AS Total_Population -- Ensure correct population handling
    FROM complete c
    JOIN worldometer_data w ON c."Country.Region" = w."Country.Region"
    WHERE w.Population > 0
    GROUP BY c.Date, w.Continent
)
SELECT 
    STRFTIME('%m/%d/%Y', Date) AS Date,
    Continent,
    COALESCE((Total_Confirmed * 100.0 / Total_Population), 0) AS Confirmed_rate,
    
    COALESCE((Total_Deaths * 100.0 / Total_Population), 0) AS Death_rate
FROM AggregatedData;
""")

# Commit the changes
conn.commit()

#Load the data into a pandas DataFrame
sql_query = "SELECT * FROM continents_rates"
df = pd.read_sql_query(sql_query, conn)

#Define the CSV file path where the table will be saved
csv_file_path = "../data/continents_rates.csv"

#Save the DataFrame as a CSV file
df.to_csv(csv_file_path, index=False)

# Close the connection
conn.close()