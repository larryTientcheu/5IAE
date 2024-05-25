import pandas as pd
import json
import random
from datetime import datetime, timedelta

# Sample data to simulate the dataset
airlines = ["United Airlines", "Delta Air Lines", "American Airlines", "Southwest Airlines"]
airports = [
    {"name": "Los Angeles International Airport", "code": "LAX", "city": "Los Angeles", "state": "California"},
    {"name": "John F. Kennedy International Airport", "code": "JFK", "city": "New York", "state": "New York"},
    {"name": "O'Hare International Airport", "code": "ORD", "city": "Chicago", "state": "Illinois"},
    {"name": "Hartsfield-Jackson Atlanta International Airport", "code": "ATL", "city": "Atlanta", "state": "Georgia"},
]

# Generate random flights data
flights_data = []
for _ in range(100):  # Generating 100 flight records
    airline = random.choice(airlines)
    departure_airport = random.choice(airports)
    destination_airport = random.choice(airports)
    
    while departure_airport == destination_airport:
        destination_airport = random.choice(airports)
    
    date_depart = datetime.now() + timedelta(days=random.randint(1, 365))
    time_depart = datetime.now() + timedelta(hours=random.randint(1, 24))
    
    flight = {
        "compagnie": airline,
        "date_depart": date_depart.strftime("%Y-%m-%d"),
        "heure_depart": time_depart.strftime("%H:%M"),
        "aeroport_origine": departure_airport["name"],
        "code_aeroport_origine": departure_airport["code"],
        "ville_origine": departure_airport["city"],
        "etat_origine": departure_airport["state"],
        "aeroport_destination": destination_airport["name"],
        "code_aeroport_destination": destination_airport["code"],
        "ville_destination": destination_airport["city"],
        "etat_destination": destination_airport["state"]
    }
    
    flights_data.append(flight)

# Convert to JSON
flights_json = json.dumps(flights_data, indent=4)
flights_json_path = 'flights_data.json'
with open(flights_json_path, 'w') as f:
    f.write(flights_json)

print(f"Sample flight data generated and saved to {flights_json_path}.")
