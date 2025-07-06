# tools/weather.py

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY", "7bb409f0d7085f86051c266d5b078272")
ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"

def getCords(city: str):
    """Geocode a city name to (lat, lon) via OpenWeatherMap Geocoding API."""
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": API_KEY}
    resp = requests.get(geo_url, params=params).json()
    if not resp:
        raise ValueError(f"Could not geocode city: {city}")
    return resp[0]["lat"], resp[0]["lon"]

def get_5day_forecast(city: str):
    """
    Fetch the next 5 days of daily forecast for `city`.
    Returns a list of dicts with:
     - date (YYYY-MM-DD)
     - feels_like
     - temp_min, temp_max
     - wind_speed
     - humidity
     - rain (mm)
     - snow (mm)
     - clouds (%)
     - sunrise, sunset (HH:MM)
     - description (weather[0].description)
    """
    lat, lon = getCords(city)
    params = {
        "lat": lat,
        "lon": lon,
        "exclude": "current,minutely,hourly,alerts",
        "units": "metric",
        "appid": API_KEY
    }
    data = requests.get(ONECALL_URL, params=params).json()
    daily = data.get("daily", [])
    forecast = []

    for day_data in daily[1:6]:  # skip today (index 0), take next 5 days
        date = datetime.utcfromtimestamp(day_data["dt"]).strftime("%Y-%m-%d")
        weather = day_data.get("weather", [{}])[0]
        forecast.append({
            "date": date,
            "feels_like": day_data["feels_like"]["day"],
            "temp_min": day_data["temp"]["min"],
            "temp_max": day_data["temp"]["max"],
            "wind_speed": day_data.get("wind_speed"),
            "humidity": day_data.get("humidity"),
            "rain_mm": day_data.get("rain", 0.0),
            "snow_mm": day_data.get("snow", 0.0),
            "clouds_pct": day_data.get("clouds"),
            "sunrise": datetime.utcfromtimestamp(day_data["sunrise"]).strftime("%H:%M"),
            "sunset": datetime.utcfromtimestamp(day_data["sunset"]).strftime("%H:%M"),
            "description": weather.get("description", "")
        })

    return forecast

print(get_5day_forecast("Lonavala"))