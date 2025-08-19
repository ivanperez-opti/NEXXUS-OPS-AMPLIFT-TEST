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
mutation DeleteAirport{
  deleteAirport(input: {id: "7d6b1e7e-7cb2-431d-a34b-d26eacc5d828"}) {
    id
    city_code
    country_code
    icao_code
    name
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
