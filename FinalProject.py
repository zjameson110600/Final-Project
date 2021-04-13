import unittest
import sqlite3
import requests
import json
import os

#
# By: Zita Jameson, Grace Coleman, Giselle Ciulla
#

def get_data_from_COVID19(country):
     url = 'https://coronavirus-19-api.herokuapp.com/countries'
     parameters = {'country': country}
     request = requests.get(url, params = parameters)
     result = request.json()
     return result

def get_data_from_MEDIAGROUP(country):
    url = 'https://covid-api.mmediagroup.fr/v1/cases'
    parameters = {'country': country}
    request = requests.get(url, params = parameters)
    result = request.json()
    return result

def get_data_from_Q(country):
    url = 'https://public.api.quarantine.country/summary/region'
    parameters = {'region': country}
    request = requests.get(url, params = parameters)
    result = request.json()
    return result


def main():
    get_data_from_COVID19('USA')
    get_data_from_MEDIAGROUP('France')
    get_data_from_Q('usa')

main()