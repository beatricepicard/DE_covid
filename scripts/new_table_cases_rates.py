import sqlite3
import pandas as pd

"""This code:
1) Removes duplicates based on (Date, Country, Confirmed, Deaths, Recovered, Active)
2) Aggregates (SUM) values for Confirmed, Deaths, Recovered, Active where (Date, Country) are the same
3) Computes rates by dividing aggregated values by Population and multiplying by 100
4) Inserts the results into the created Cases_rates table in covid_database"""

# Define database path
db_path = "../data/covid_database.db"

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop the existing table (for testing purposes)
cursor.execute("DROP TABLE IF EXISTS Cases_rates")

# Create the Cases_rates table
cursor.execute("""
CREATE TABLE Cases_rates (
    Date TEXT NOT NULL,  -- Stored in MM/DD/YYYY format
    Country TEXT NOT NULL,
    Continent TEXT,
    Confirmed_Rate REAL,
    Deaths_Rate REAL,
    Recovered_Rate REAL,
    Active_Rate REAL,               
    PRIMARY KEY (Date, Country)
);
""")

# SQL Query with Deduplicated Data
sql_insert = """
WITH DeduplicatedData AS (
    SELECT 
        c.Date,
        c.[Country.Region] AS Country,
        w.Continent,
        SUM(c.Confirmed) AS Total_Confirmed,
        SUM(c.Deaths) AS Total_Deaths,
        SUM(c.Recovered) AS Total_Recovered,
        SUM(c.Active) AS Total_Active,
        w.Population
    FROM complete c
    JOIN worldometer_data w ON c.[Country.Region] = w.[Country.Region]
    WHERE w.Population > 0
    GROUP BY c.Date, c.[Country.Region]
)

-- Insert aggregated and calculated rates into Cases_rates table
INSERT INTO Cases_rates (Date, Country, Continent, Confirmed_Rate, Deaths_Rate, Recovered_Rate, Active_Rate)
SELECT 
    STRFTIME('%m/%d/%Y', Date) AS Date,  -- Convert to MM/DD/YYYY format
    Country,
    Continent,
    COALESCE((Total_Confirmed * 100.0 / Population), 0) AS Confirmed_Rate,
    COALESCE((Total_Deaths * 100.0 / Population), 0) AS Deaths_Rate,
    COALESCE((Total_Recovered * 100.0 / Population), 0) AS Recovered_Rate,
    COALESCE((Total_Active * 100.0 / Population), 0) AS Active_Rate
FROM DeduplicatedData;
"""

# Execute the SQL query
cursor.executescript(sql_insert)

# Commit and close the connection
conn.commit()

#Load the data into a pandas DataFrame
#sql_query = "SELECT * FROM Cases_rates"
#df = pd.read_sql_query(sql_query, conn)

#Define the CSV file path where the table will be saved
#csv_file_path = "../data/cases_rates.csv"

#Save the DataFrame as a CSV file
#df.to_csv(csv_file_path, index=False)

#Close the database connection
conn.close()