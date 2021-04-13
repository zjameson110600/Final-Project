import unittest
import sqlite3
import requests
import json
import os

#
# By: Zita Jameson, Grace Coleman, Giselle Ciulla
#

def cases_deaths():
    url = 'https://coronavirus-19-api.herokuapp.com/countries'
    request = requests.get(url)
    result = request.json()
    for country in result:
        countries = country['country']
        cases = country['cases']
        deaths = country['deaths']
        cases_per_mil = country['casesPerOneMillion']
        deaths_per_mil = country['deathsPerOneMillion']

def population_location():
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
            #print(countries + ": " + str(population) + " " +  str(latitude) + " " + str(longitude))
            complete.append(countries)
        except:
            #print(countries + ": value(s) unavailable")
            incomplete.append(countries)
    print(complete)
    print(incomplete)


def testing():
    url = 'https://api.quarantine.country/api/v1/summary/latest'
    request = requests.get(url)
    result = request.json()
    for x in result:
        test = result['data']['regions']
        for x in test:
            try:
                tested = x['tested']
            except:
                print('No test info')
    print(tested)


def main():
    cases_deaths()
    population_location()
    testing()

main()
