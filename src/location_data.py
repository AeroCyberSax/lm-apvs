import requests
from typing import Optional, Tuple
from geopy.geocoders import Nominatim

def get_lat_long_from_ip() -> Optional[Tuple[float, float]]:
    try:
        response = requests.get('https://ipinfo.io/')
        data = response.json()
        loc = data.get('loc')
        if loc:
            latitude, longitude = loc.split(',')
            return float(latitude), float(longitude)
        else:
            raise ValueError("Location data not found in response.")
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to connect to the location service: {e}")
    except ValueError as e:
        raise ValueError(f"Error processing location data: {e}")
    
def get_location_from_lat_long(latitude: float, longitude: float):
    geolocator = Nominatim(user_agent="lm-avps")
    location = geolocator.reverse((latitude, longitude), language='en')
    if location and 'address' in location.raw:
        address = location.raw['address']
        city = address.get('city') or address.get('town') or address.get('village') or ''
        state = address.get('state', '')

        return f"{city}, {state}"
    else:
        raise ValueError("Could not retrieve location information from coordinates.")