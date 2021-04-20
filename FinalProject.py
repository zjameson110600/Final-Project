import unittest
import sqlite3
import requests
import json
import os
import csv

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
    country_count = 0
    cur.execute("CREATE TABLE IF NOT EXISTS Countries (country TEXT PRIMARY KEY, cases INTEGER, deaths INTEGER)")
    for country in result:
        countries = country['country']
        cases = country['cases']
        deaths = country['deaths']
        if country_count == 25:
            break
        if cur.execute("SELECT country FROM Countries WHERE country = ?", (countries,)).fetchone() == None:
            cur.execute("INSERT OR REPLACE INTO Countries (country,cases,deaths) VALUES (?,?,?)", (countries, cases, deaths))
            country_count += 1
            continue
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
    pop_count = 0
    cur.execute("CREATE TABLE IF NOT EXISTS Populations (country TEXT PRIMARY KEY, continent TEXT, population INTEGER, latitude FLOAT, longitude FLOAT)")
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
        if pop_count == 25:
            break
        if cur.execute("SELECT country FROM Populations WHERE country = ?", (countries,)).fetchone() == None:
            cur.execute("INSERT OR REPLACE INTO Populations (country, continent, population, latitude, longitude) VALUES (?,?,?,?,?)",(countries, continent, population, lat, long))
            pop_count += 1
            continue
    conn.commit()
    for c in continent_list:
        continents[c] = continents.get(c, 0) + 1
        #number_of_countries = continents[c]
    cont_count = 0
    for i in continents:
        if cont_count == 25:
            break
        if cur.execute("SELECT continent FROM Continent_Info WHERE continent = ?", (i[0],)).fetchone() == None:
            cur.execute("INSERT OR REPLACE INTO Continent_Info (continent, number_of_countries) VALUES (?,?)", (i, continents[i]))
            cont_count += 1
            continue
    conn.commit()


def testing(cur, conn):
    # returns the amount of people tested in each country
    url = 'https://api.quarantine.country/api/v1/summary/latest'
    request = requests.get(url)
    result = request.json()
    continent_count = 0
    cur.execute("CREATE TABLE IF NOT EXISTS Tested (country TEXT PRIMARY KEY, tested INTEGER)")
    for x in result:
        test = result['data']['regions']
        for x in test:
            countries = x
            tested = test[x]['tested']
            if continent_count == 25:
                break
            if cur.execute("SELECT continent FROM Continent_Info WHERE continent = ?", (x[0],)).fetchone() == None:
                cur.execute("INSERT OR REPLACE INTO Tested (country, tested) VALUES (?,?)", (countries,tested))
                continent_count += 1
            continue
    conn.commit()


def calculate_countries(cur, conn):
    with open('calculations.csv', mode='w') as f:
<<<<<<< HEAD
        write = csv.writer(f, delimiter=',', quotechar='"')
        countries = cur.execute("SELECT country FROM Countries")
        cases = cur.execute("SELECT cases FROM Countries")
        deaths = cur.execute("SELECT deaths FROM Countries")
        death_rate = (cases)/(deaths)
        write.writerow(['Country', 'Cases', 'Deaths', 'Death Rate'])
=======
        writer = csv.writer(f)
        countries = cur.execute("SELECT country FROM Countries")
        cases = cur.execute("SELECT cases FROM Countries")
        deaths = cur.execute("SELECT deaths FROM Countries")
        cur.fetchall()
        for x in countries:
            death_rate = cases/deaths
        writer.writerow(['Country', 'Cases', 'Deaths', 'Death Rate'])
>>>>>>> fd14f586457163ad86c148da3137c9fb8e2475ca
        for x in countries:
            write.writerow([x, cases, deaths, death_rate])
    return death_rate


def main():
    cur, conn = setupDatabase('covid_d.db')
    cases_deaths(cur, conn)
    population_location(cur, conn)
    testing(cur, conn)
    calculate_countries(cur, conn)

if __name__ == '__main__':
    main()
