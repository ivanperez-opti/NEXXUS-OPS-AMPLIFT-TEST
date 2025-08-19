import csv
import requests

# Reemplaza estos valores con los de tu proyecto Amplify
API_URL = "https://tdno4cnrjfe67dbh77pauwzk3u.appsync-api.us-east-1.amazonaws.com/graphql"
API_KEY = "da2-vddgjuwhdnfq7ajpf6a6fjoduu"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

# Mutación GraphQL para crear un aeropuerto
mutation = """
mutation CreateAirport($input: CreateAirportInput!) {
  createAirport(input: $input) {
    id
    station_code
    icao_code
    name
  }
}
"""

# Leer el archivo CSV y enviar cada fila como mutación
with open("Amplify/AirportOperations/airports.csv", newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        variables = {
            "input": {
                "station_code": row["station_code"],
                "icao_code": row["icao_code"],
                "name": row["name"],
                "country_code": row["country_code"],
                "city_code": row["city_code"],
                "market_code": row["market_code"],
                "region": row["region"],
                "timezone": row["timezone"]
            }
        }

        response = requests.post(API_URL, headers=headers, json={
            "query": mutation,
            "variables": variables
        })

        if response.status_code == 200:
            result = response.json()
            if "errors" in result:
                print("❌ Error en mutación:", result["errors"])
            else:
                airport = result["data"]["createAirport"]
                print(f"✅ Insertado: {airport['station_code']} - {airport['name']}")
        else:
            print("❌ Error HTTP:", response.status_code, response.text)
