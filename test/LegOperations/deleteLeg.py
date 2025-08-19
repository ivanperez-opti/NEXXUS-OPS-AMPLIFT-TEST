import csv
import requests
import json

API_URL = "https://tdno4cnrjfe67dbh77pauwzk3u.appsync-api.us-east-1.amazonaws.com/graphql"
API_KEY = "da2-vddgjuwhdnfq7ajpf6a6fjoduu"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

# Mutación GraphQL (con variables)
mutation = """
mutation DeleteLeg{
  deleteLeg(input: {id: "dc529443-24ec-400f-abe8-11039fe0f9bc"}) {
    id
    uuid
    author
    arrival_station
  }
}
"""

# Arma el payload
payload = {
    "query": mutation,
}

# Envía la petición POST a AppSync
response = requests.post(API_URL, headers=headers, json=payload)

# Imprime la respuesta
print(json.dumps(response.json(), indent=2))
