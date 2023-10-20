from pprint import pprint

from requests import request

response = request(url='https://jservice.io/api/random?count=1', method='GET')
if response.status_code == 200:
    pprint(response.json())