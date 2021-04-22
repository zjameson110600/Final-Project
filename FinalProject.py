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
    count = 0
    cur.execute("CREATE TABLE IF NOT EXISTS Populations (country TEXT PRIMARY KEY, country_id INTEGER, continent TEXT, population INTEGER, latitude FLOAT, longitude FLOAT)")
    conn.commit()
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
        for x in complete:
            if pop_count == 25:
                break
            if cur.execute("SELECT country FROM Countries WHERE country = ?", (x,)).fetchone() == None:
                cur.execute("INSERT OR REPLACE INTO Populations (country, country_id, continent, population, latitude, longitude) VALUES (?,?,?,?,?,?)",(countries.lower(), count, continent, population, lat, long))
                pop_count += 1
                count += 1
                continue
    conn.commit()


def testing(cur, conn):
    # returns the amount of people tested in each country
    url = 'https://api.quarantine.country/api/v1/summary/latest'
    request = requests.get(url)
    result = request.json()
    continent_count = 0
    cur.execute("CREATE TABLE IF NOT EXISTS Tested (id INTEGER PRIMARY KEY,tested INTEGER)")
    conn.commit()
    for x in result:
        test = result['data']['regions']
        for x in test:
            continents = cur.execute("SELECT continent FROM Populations").fetchall()
            conn.commit()
            countries = x.lower()
            tested = test[x]['tested']
            if continent_count == 25:
                break
            if cur.execute("SELECT country FROM Populations WHERE country = ?", (x,)).fetchone() == None:
                country = cur.execute("SELECT country_id FROM Populations WHERE country = ?", (x,)).fetchone()
                cur.execute("INSERT OR REPLACE INTO Tested (id,tested) VALUES (?,?)", (country,tested))
                conn.commit()
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
        f.writerow(['Country', 'Cases', 'Deaths', 'Death Rate'])
        for x in data:
            try:
                death_rate = (x[2]/x[1])
            except:
                death_rate = 0
            all_data = (x[0], x[1], x[2], death_rate)
            f.writerow(all_data)

def calculate_populations(cur, conn, filepath):
    #calculates infection rate and inserts data into csv
    source_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(source_dir, filepath)

    distinct = cur.execute("SELECT Countries.country, Countries.cases, Populations.population FROM Countries INNER JOIN Populations ON Countries.country = Populations.country").fetchall()
    conn.commit()

    with open(filepath, 'w') as f:
        f = csv.writer(f, delimiter = ',')
        f.writerow(['Country', 'Population', 'Cases', 'Infection Rate'])
        for x in distinct:
            infection_rate = x[1]/x[2]
            all_data = (x[0], x[2], x[1], infection_rate)
            f.writerow(all_data)

def calculate_testing(cur, conn, filepath):
    #calculates testing rate per country
    source_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(source_dir, filepath)

    testing = cur.execute("SELECT Tested.tested, Tested.id, Populations.country, Populations.population FROM Tested INNER JOIN Populations ON Tested.id = Populations.country_id").fetchall()
    conn.commit()
    #tested, id, country, population
    with open(filepath, "w") as f:
        f = csv.writer(f, delimiter= ",")
        f.writerow(['Id', 'Country', 'Tested', 'Population','Testing Rate'])
        for x in testing:
            try:
                testing_rate = x[3]/x[0]
            except:
                testing_rate = 0
            all_data= (x[1], x[2], x[0], x[3], testing_rate)
            f.writerow(all_data)



def main():
    cur, conn = setupDatabase('covid7.db')
    cases_deaths(cur, conn)
    population_location(cur, conn)
    testing(cur, conn)
    calculate_countries(cur, conn, 'calculation_countries.csv')
    calculate_populations(cur, conn, 'calculation_populations.csv')
    calculate_testing(cur, conn, 'calculation_testing.csv')

if __name__ == '__main__':
    main()
