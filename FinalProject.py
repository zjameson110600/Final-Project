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
    cur.execute("CREATE TABLE IF NOT EXISTS Populations (country TEXT PRIMARY KEY, population INTEGER, latitude FLOAT, longitude FLOAT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Life_Expectancy (country TEXT PRIMARY KEY, life_expectancy FLOAT)")
    for country in result:
        countries = country
        try:
            population = result[countries]["All"]["population"]
            lat = float(result[countries]["All"]["lat"])
            long = float(result[countries]["All"]["long"])
            life_expect = float(result[countries]['All']["life_expectancy"])
            complete.append(countries)
        except:
            incomplete.append(countries)
        cur.execute("INSERT OR REPLACE INTO Populations (country,population,latitude,longitude) VALUES (?,?,?,?)",(countries, population, lat, long))
    #conn.commit()
        cur.execute("INSERT OR REPLACE INTO Life_Expectancy (country, life_expectancy) VALUES (?,?)", (countries, life_expect))
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
            print(countries)
            tested = test[x]['tested']
            cur.execute("INSERT OR REPLACE INTO Tested (country, tested) VALUES (?,?)", (countries,tested))
            #print(cur.rowcount)
    conn.commit()


def main():
    cur, conn = setupDatabase('test_intnl_covid_rates.db')
    cases_deaths(cur, conn)
    population_location(cur, conn)
    testing(cur, conn)

if __name__ == '__main__':
    main()
