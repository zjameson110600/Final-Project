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
    for country in result:
        countries = country
        population = result['All']['population']
        lat = countries['All']['lat']
        long = countries['All']['long']

def testing():
    url = 'https://api.quarantine.country/api/v1/summary/latest'
    request = requests.get(url)
    result = request.json()
    regions = result['data']['regions']
    for x in regions:
        testing = x['tested']
    

def main():
    cases_deaths()
    population_location()
    testing()

main()
