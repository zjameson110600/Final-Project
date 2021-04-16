import unittest
import sqlite3
import requests
import json
import os

#
# By: Zita Jameson, Grace Coleman, Giselle Ciulla
#

def setupDatabase(db_name):
    # Setup Database
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def cases_deaths(cur, conn):
    # gets data from api and puts into table
    url = 'https://coronavirus-19-api.herokuapp.com/countries'
    request = requests.get(url)
    result = request.json()
    cur.execute("CREATE TABLE IF NOT EXISTS Countries (country TEXT PRIMARY KEY, cases INTEGER, deaths INTEGER)")
    for country in result:
        countries = country['country']
        cases = country['cases']
        deaths = country['deaths']
        cur.execute("INSERT OR REPLACE INTO Countries (country,cases,deaths) VALUES (?,?,?)", (countries, cases, deaths))
    conn.commit()


def population_location(cur, conn):
    # gets data from api and puts into table
    url = 'https://covid-api.mmediagroup.fr/v1/cases'
    request = requests.get(url)
    result = request.json()
    complete = []
    incomplete = []
    continents = {}
    continent_list = []
    none = []
    cur.execute("CREATE TABLE IF NOT EXISTS Populations (continent TEXT PRIMARY KEY, country TEXT, population INTEGER, latitude FLOAT, longitude FLOAT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Continent_Info (continent TEXT PRIMARY KEY, number_of_countries INTEGER)")
    for country in result:
        countries = country
        try:
            continent = result[countries]["All"]["continent"]
            continent_list.append(continent)
        except:
            none.append(continent)
        try:
            population = result[countries]["All"]["population"]
            lat = float(result[countries]["All"]["lat"])
            long = float(result[countries]["All"]["long"])
            complete.append(countries)
        except:
            incomplete.append(countries)
    for c in continent_list:
        continents[c] = continents.get(c, 0) + 1
        #number_of_countries = continents[c]
    cur.execute("INSERT OR REPLACE INTO Populations (continent, country, population, latitude, longitude) VALUES (?,?,?,?,?)",(continent, countries, population, lat, long))
        # asia = cur.execute("SELECT country FROM Populations WHERE continent = 'Asia'")
        # europe = cur.execute("SELECT country FROM Populations WHERE continent = 'Europe'")
        # south_america = cur.execute("SELECT country FROM Populations WHERE continent = 'South America'")
        # north_america = cur.execute("SELECT country FROM Populations WHERE continent = 'North America'")
        # africa = cur.execute("SELECT country FROM Populations WHERE continent = 'Africa'")
        # oceania = cur.execute("SELECT country FROM Populations WHERE continent = 'Oceania'")
    cur.execute("INSERT OR REPLACE INTO Continent_Info (continent, number_of_countries) VALUES (?,?)", (continent, continents[continent]))
    conn.commit()


def testing(cur, conn):
    # returns the amount of people tested in each country
    url = 'https://api.quarantine.country/api/v1/summary/latest'
    request = requests.get(url)
    result = request.json()
    cur.execute("CREATE TABLE IF NOT EXISTS Tested (country TEXT PRIMARY KEY, tested INTEGER)")
    for x in result:
        test = result['data']['regions']
        for x in test:
            countries = x
            tested = test[x]['tested']
            cur.execute("INSERT OR REPLACE INTO Tested (country, tested) VALUES (?,?)", (countries,tested))
    conn.commit()


def main():
    cur, conn = setupDatabase('intnl_covid_rates.db')
    cases_deaths(cur, conn)
    population_location(cur, conn)
    testing(cur, conn)

if __name__ == '__main__':
    main()
