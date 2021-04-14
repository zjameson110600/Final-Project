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
    return cur, ConnectionResetError


def cases_deaths(cur, conn):
    # gets data from api and puts into table
    url = 'https://coronavirus-19-api.herokuapp.com/countries'
    request = requests.get(url)
    result = request.json()
    for country in result:
        countries = country['country']
        cases = country['cases']
        deaths = country['deaths']
    cur.execute("DROP TABLE IF EXISTS Countries")
    cur.execute("CREATE TABLE Countries (country TEXT PRIMARY KEY, cases INTEGER, deaths INTEGER)")
    for i in range(len(countries)):
        cur.execute("INSERT INTO Countries (country,cases,deaths) VALUES (?,?,?)",(i, cases, deaths))
    conn.commit()


def population_location(cur, conn):
    # gets data from api and puts into table
    url = 'https://covid-api.mmediagroup.fr/v1/cases'
    request = requests.get(url)
    result = request.json()
    complete = []
    incomplete = []
    for country in result:
        countries = country
        try:
            population = result[countries]["All"]["population"]
            lat = result[countries]["All"]["lat"]
            long = result[countries]["All"]["long"]
            complete.append(countries)
        except:
            incomplete.append(countries)
    cur.execute("DROP TABLE IF EXISTS Populations")
    cur.execute("CREATE TABLE Populations (country TEXT PRIMARY KEY, population INTEGER, latitude INTEGER, longitude INTEGER)")
    cur.execute("INSERT INTO Populations (country,population,latitude,longitude) VALUES (?,?,?)",(countries, population, lat, long))
    conn.commit()


def testing():
    # returns the amount of people tested in each country
    url = 'https://api.quarantine.country/api/v1/summary/latest'
    request = requests.get(url)
    result = request.json()
    for x in result:
        test = result['data']['regions']
        countries = x
        for x in test:
            try:
                tested = result['data']['regions'][x]['tested']
            except:
                print('No test info')
        return (countries, tested)
    cur.execute("DROP TABLE IF EXISTS Tested")
    cur.execute("CREATE TABLE Tested (country TEXT PRIMARY KEY, population INTEGER, tested INTEGER)")
    cur.execute("INSERT INTO Tested (country,population,latitude,longitude) VALUES (?,?,?)",(countries, population, tested))
    conn.commit()



def main():
    cur, conn = setupDatabase('intnl_covid_rates.db')
    cases_deaths(cur, conn)
    population_location(cur, conn)
    testing(cur, conn)

if __name__ == '__main__':
    main()
