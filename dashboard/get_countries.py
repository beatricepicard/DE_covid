import sqlite3
import pandas as pd 


#Holt alle Länder aus der Datenbank.
def get_countries():
    db_path = "../data/covid_database.db"
    connection = sqlite3.connect(db_path)
    query = "SELECT DISTINCT \"Country.Region\" FROM country_wise"
    countries = pd.read_sql(query, connection)["Country.Region"].tolist()
    connection.close()
    return countries