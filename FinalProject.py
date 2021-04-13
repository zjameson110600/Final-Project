import unittest
import sqlite3
import requests
import json
import os

#
# By: Zita Jameson, Grace Coleman, Giselle Ciulla
#

def get_data_from_COVID19(from_date, to_date, country):
    url = 'https://api.covid19api.com/country/{country}/status/confirmed?from={from_date}&to={to_date}}'
    parameters = {'country': country, 'from': from_date, 'to': to_date}
    request = requests.get(url, params = parameters)
    result = request.json()
    return result

def get_data_from_MEDIAGROUP(country):
    url = 'https://covid-api.mmediagroup.fr/v1'
    parameters = {'country': country}
    request = requests.get(url, params = parameters)
    result = request.json()
    return result

def get_data_from_Q(country):
    url = 'https://public.api.quarantine'
    parameters = {'country': country}
    request = requests.get(url, params = parameters)
    result = request.json()
    return result

get_data_from_COVID19('2020-07-03T00:00:00Z','2020-07-04T00:00:00Z', 'United States')
get_data_from_MEDIAGROUP('France')
get_data_from_Q('usa')