import unittest
import sqlite3
import requests
import json
import os

#
# By: Zita Jameson, Grace Coleman, Giselle Ciulla
#

def cases_deaths():
    # returns cases, deaths, cases per mil, deaths per mil in each country
    url = 'https://coronavirus-19-api.herokuapp.com/countries'
    request = requests.get(url)
    result = request.json()
    dict = {}
    for country in result:
        countries = country['country']
        cases = country['cases']
        deaths = country['deaths']
    dict[countries] = [cases, deaths]
    return dict
    

def population_location():
    # returns population, longitude, latitude for each country
    url = 'https://covid-api.mmediagroup.fr/v1/cases'
    request = requests.get(url)
    result = request.json()
    complete = []
    incomplete = []
    for country in result:
        countries = country
        try:
            population = result[countries]["All"]["population"]
            latitude = result[countries]["All"]["lat"]
            longitude = result[countries]["All"]["long"]
            complete.append(countries)
        except:
            incomplete.append(countries)
        return (countries, population, latitude, longitude)

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

def setupDatabase(db_name):
    # Setup Database
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, ConnectionResetError

def create_countries_table(cur, conn):
    # Setup countries in database
    values = cases_deaths
    country = values.keys()
    for x in values.items():
        cases = values.items()[0]
        deaths = values.items()[1]
    cur.execute("DROP TABLE IF EXISTS Countries")
    cur.execute("CREATE TABLE Countries (country TEXT PRIMARY KEY, cases INTEGER, deaths INTEGER)")
    cur.execute("INSERT INTO Countries (country,cases,deaths) VALUES (?,?,?)",(country, cases, deaths))
    conn.commit()

def main():
    cur, conn = setupDatabase('intnl_covid_rates.db')
    create_countries_table(cur, conn)

if __name__ == '__main__':
    main()
