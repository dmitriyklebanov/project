import json
import requests


API_URL = 'https://api.exchangeratesapi.io/latest?base=USD'


def get_currency_rate(from_label, to_label):
    response = requests.get(API_URL, timeout=2)
    rates = json.loads(response.content)['rates']
    return rates[to_label] / rates[from_label]
