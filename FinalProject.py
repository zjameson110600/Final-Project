import unittest
import sqlite3
import requests
import json
import os

#
# By: Zita Jameson, Grace Coleman, Giselle Ciulla
#

def get_data_from_COVID19():
    url = 'https://coronavirus-19-api.herokuapp.com/countries'
    request = requests.get(url)
    result = request.json()
    for c in result:
        countries = c['country']
        cases = c['cases']
        deaths = c['deaths']
        cases_per_mil = c['casesPerOneMillion']
        deaths_per_mil = c['deathsPerOneMillion']

def get_data_from_MEDIAGROUP():
    url = 'https://covid-api.mmediagroup.fr/v1/cases'
    request = requests.get(url)
    result = request.json()
    return result

def get_data_from_Q():
    url = 'https://api.quarantine.country/api/v1/summary/latest'
    request = requests.get(url)
    result = request.json()
    for c in result['data']['regions']:
        countries = c['name']
        cases = c['total_cases']
        deaths = c['deaths']
        death_ratio = c['death_ratio']
    print(result)


def main():
    get_data_from_COVID19()
    get_data_from_MEDIAGROUP()
    get_data_from_Q()

main()
