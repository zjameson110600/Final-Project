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
    cont_count = 0


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


def calculate_countries(cur, conn, filepath):
    #calculates death rate and inserts data into csv
    source_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(source_dir, filepath)

    data = cur.execute("SELECT country,cases,deaths FROM Countries").fetchall()
    conn.commit()

    with open(filepath, 'w') as f:
        f = csv.writer(f, delimiter = ',')
        for x in data:
            try:
                death_rate = (x[2]/x[1])
            except:
                death_rate = 0
            all_data = (x[0], x[1], x[2], death_rate)
            f.writerow(['Country', 'Cases', 'Deaths', 'Death Rate'])
            f.writerow(all_data)

def calculate_populations(cur, conn, filepath):
    #calculates infection rate and inserts data into csv
    source_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(source_dir, filepath)

    distinct = cur.execute("SELECT Countries.country, Countries.cases, Populations.population FROM Countries INNER JOIN Populations ON Countries.country = Populations.country").fetchall()
    conn.commit()

    with open(filepath, 'w') as f:
        f = csv.writer(f, delimiter = ',')
        for x in distinct:
            infection_rate = x[1]/x[2]
            all_data = (x[0], x[2], x[1], infection_rate)
            f.writerow(['Country', 'Population', 'Cases', 'Infection Rate'])
            f.writerow(all_data)

def calculate_testing(cur, conn, filepath):
    #calculates testing rate per country
    source_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(source_dir, filepath)

    testing = cur.execute("SELECT Populations.country, Populations.population, Tested.tested FROM Populations INNER JOIN Tested ON Populations.country = Tested.country").fetchall()
    conn.commit()
    with open(filepath, "w") as f:
        f=csv.writer(f, delimiter= ",")
        for x in testing:
            testing_rate= x[1]/x[2]
            all_data= (x[0], x[2], x[1], testing_rate)
            f.writerow(['Country', 'Population', 'Tested', "Testing Rate"])
            f.writerow(all_data)




def main():
    cur, conn = setupDatabase('covid_d.db')
    cases_deaths(cur, conn)
    population_location(cur, conn)
    testing(cur, conn)
    calculate_countries(cur, conn, 'calculation_countries.csv')
    calculate_populations(cur, conn, 'calculation_populations.csv')
    calculate_testing(cur, conn, 'calculation_testing.csv')

if __name__ == '__main__':
    main()
