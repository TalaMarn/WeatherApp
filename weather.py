import os
import requests

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):

    if not API_KEY:
        raise ValueError("OpenWeather API key is missing.")

    # Step 1: Get city coordinates
    geo_params = {
        "q": city,
        "limit" : 1,
        "appid" : API_KEY
    }

    geo_response = requests.get(
        GEO_URL,
        params=geo_params,
        timeout=10
    )

    geo_response.raise_for_status()

    locations = geo_response.json()

    if not locations:
        raise ValueError("City not found.")

    latitude = locations[0]["lat"]
    longitude = locations[0]["lon"]

    # Step 2: Get current weather
    weather_params = {
        "lat": latitude,
        "lon": longitude,
        "appid": API_KEY,
        "units": "metric"
    }

    weather_response = requests.get(
        WEATHER_URL,
        params=weather_params,
        timeout=10
    )

    weather_response.raise_for_status()

    data = weather_response.json()

    # Step 3: Extract useful infomation
    weather_info = {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data["wind"]["speed"],
        "description": data["weather"][0]["description"],
        "main": data["weather"][0]["main"]
    }

    return weather_info

# Test the weather API

if __name__ == "__main__":

    try:
        result = get_weather("Chiang Mai")

        print("Weather Information")
        print("-------------------")

        for key, value in result.items():
            print(f"{key}: {value}")

    except requests.exceptions.RequestException as error:
        print("API connection error:", error)

    except ValueError as error:
        print("ERROR:", error)