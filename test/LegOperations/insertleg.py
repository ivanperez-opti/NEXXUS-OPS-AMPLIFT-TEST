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

# Mutación GraphQL para crear un aeropuerto
mutation = """
mutation CreateLeg($input: CreateLegInput!) {
  createLeg(input: $input) {
    uuid
    departure_date
    company_code
    departure_station
    arrival_station
    author
    expiration
  }
}
"""

# Leer el archivo CSV y enviar cada fila como mutación
with open("leg_table_10.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        variables = {
            "input": {
                "uuid": row["uuid"],
                "departure_date": row["departure_date"],
                "company_code": row["company_code"],
                "number": row["number"],
                "departure_station": row["departure_station"],
                "arrival_station": row["arrival_station"],
                "scheduled_departure": row["scheduled_departure"],
                "scheduled_arrival": row["scheduled_arrival"],
                "service_type": row["service_type"],
                "aircraft_type": row["aircraft_type"],
                "author": row["author"],
                "source": row["source"],
                "timestamp": row["timestamp"],
                "expiration": int(row["expiration"])  
            }
        }

        response = requests.post(API_URL, headers=headers, json={
            "query": mutation,
            "variables": variables
        })

        if response.status_code == 200:
            result = response.json()
            if "errors" in result:
                print("Error en mutación:", result["errors"])
            else:
                airport = result["data"]["createLeg"]
                print(f"Insertado: {airport['uuid']}")
        else:
            print("Error HTTP:", response.status_code, response.text)
