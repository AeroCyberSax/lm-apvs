from time import sleep
from location_data import get_lat_long_from_ip, get_location_from_lat_long
from adsb_query import get_near_aircraft_data, nearest_aircraft_query
import json
import os

def main():
    try:
        latitude, longitude = get_lat_long_from_ip()
        try:
            user_location = get_location_from_lat_long(latitude, longitude)
            print(f"Detected user location (approximate): {user_location} ({latitude}, {longitude})")
        except ValueError as e:
            print(f"Could not retrieve location information: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    #print(get_military_aircraft_data())
    with open("./src/lockheed_types.json") as f:
        LOCKHEED_TYPES = json.load(f)

    while True:
        """if os.name == 'nt':  # 'nt' refers to Windows
            os.system('cls')
        else:  # 'posix' refers to Linux/macOS
            os.system('clear')"""
        nearest_aircraft_query(get_near_aircraft_data(latitude, longitude), LOCKHEED_TYPES)
        sleep(1) # Fastest time is 1 query per second to avoid rate limiting

if __name__ == "__main__":
    main()