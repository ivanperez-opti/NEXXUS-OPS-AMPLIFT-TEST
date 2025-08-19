import csv
import requests
import json

# Reemplaza estos valores con los de tu proyecto Amplify
API_URL = "https://tdno4cnrjfe67dbh77pauwzk3u.appsync-api.us-east-1.amazonaws.com/graphql"
API_KEY = "da2-vddgjuwhdnfq7ajpf6a6fjoduu"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

# Mutación GraphQL (con variables)
mutation = """
mutation UpdateLeg {
  updateLeg(input: {
    id: "7b8927a7-ed49-4a15-8c9e-880b7138f6b3"
    author: "OscarPerez"
    arrival_station: "LAX"
  }) {
    id
    uuid
    author
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
