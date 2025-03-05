import sqlite3
import pandas as pd

path = r"..\data\covid_database.db"
conn = sqlite3.connect(path)
cursor = conn.cursor()

cursor.execute("""
    SELECT c."Country.Region"
    FROM complete c
    LEFT JOIN worldometer_data w ON c."Country.Region" = w."Country.Region"
    WHERE w.Population IS NULL;
""")

missing_list = [row[0] for row in cursor.fetchall()]

population_data = {
    'Burma': 54179306,  
    'Central African Republic': 5454533,
    'China': 1425893465,
    'Congo (Brazzaville)': 5798805,  
    'Congo (Kinshasa)': 102262808,  
    "Cote d'Ivoire": 28715666,  
    'Holy See': 800,  
    'Kosovo': 1935259,
    'Saint Vincent and the Grenadines': 104332,
    'South Korea': 51815810,
    'United Arab Emirates': 9991089,
    'United Kingdom': 67508936,
    'US': 339996563,  
    'West Bank and Gaza': 5438616
}

for country, population in population_data.items():
    cursor.execute("INSERT INTO worldometer_data (\"Country.Region\", Population) VALUES (?, ?)", (country, population))
    
conn.commit()
conn.close()