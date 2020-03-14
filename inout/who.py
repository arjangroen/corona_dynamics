import requests
import json
import pandas as pd

endpoint = "https://corona.lmao.ninja/countries"

def get_all():
    return requests.get(endpoint).json()



resp = get_all()
print('')

