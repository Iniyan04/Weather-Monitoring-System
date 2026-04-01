import requests


def fetch_weather_from_api(city: str):
    """
    Using Open-Meteo (no API key required)
    """
    # Step 1: Get latitude & longitude from city name
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo_response = requests.get(geo_url).json()

    if "results" not in geo_response:
        return None

    lat = geo_response["results"][0]["latitude"]
    lon = geo_response["results"][0]["longitude"]

    # Step 2: Get weather data
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    weather_response = requests.get(weather_url).json()

    if "current_weather" not in weather_response:
        return None

    return {
        "temperature": weather_response["current_weather"]["temperature"],
        "humidity": 50,  # Open-Meteo doesn't give humidity directly here
        "date": weather_response["current_weather"]["time"]
    }