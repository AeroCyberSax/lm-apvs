import requests

def get_near_aircraft_data(latitude: float, longitude: float, distance_nm: int = 250) -> dict:
    try:
        response = requests.get(f'https://opendata.adsb.fi/api/v2/lat/{latitude}/lon/{longitude}/dist/{distance_nm}')
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise ConnectionError(f"Failed to connect to the military aircraft data service: {e}")
    except ValueError as e:
        raise ValueError(f"Error processing military aircraft data: {e}")
    
def nearest_aircraft_query(data, LOCKHEED_TYPES):
    aircraft_list = data.get("aircraft", [])
    closest = None

    for aircraft in aircraft_list:
        t_value = aircraft.get("t", "")

        if t_value in LOCKHEED_TYPES:
            dst = aircraft.get("dst", float('inf'))

            # If we haven't found one yet or this one is closer
            if closest is None or dst < closest["dst"]:
                closest = {
                    "t": t_value,
                    "desc": aircraft.get("desc", "N/A"),
                    "callsign": aircraft.get("flight", "N/A"),
                    "lat": aircraft.get("lat"),
                    "lon": aircraft.get("lon"),
                    "dst": dst,
                    "alt_baro": aircraft.get("alt_baro", "N/A"),
                }

    # Output closest aircraft info
    if closest:
        print(f"Closest Lockheed Aircraft:"
              f"\n  Type: {closest['t']}"
              f"\n  Description: {closest['desc']}"
              f"\n  Callsign: {closest['callsign']}"
              f"\n  Distance: {closest['dst']} NM"
              f"\n  Barometric Altitude: {closest['alt_baro']} ft")
    else:
        print("No Lockheed aircraft found nearby.")
