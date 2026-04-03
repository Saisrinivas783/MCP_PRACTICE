from fastapi import FastAPI, HTTPException
from datetime import date, timedelta

app = FastAPI(title="Weather API", version="1.0.0")

WEATHER_DATA = {
    "london": {
        "temperature": 12.5,
        "condition": "Cloudy",
        "forecast": [
            {"date": str(date.today() + timedelta(days=1)), "high": 14, "low": 9,  "condition": "Rainy"},
            {"date": str(date.today() + timedelta(days=2)), "high": 11, "low": 7,  "condition": "Cloudy"},
            {"date": str(date.today() + timedelta(days=3)), "high": 13, "low": 8,  "condition": "Partly Cloudy"},
            {"date": str(date.today() + timedelta(days=4)), "high": 15, "low": 10, "condition": "Sunny"},
            {"date": str(date.today() + timedelta(days=5)), "high": 16, "low": 11, "condition": "Sunny"},
        ],
    },
    "new york": {
        "temperature": 18.3,
        "condition": "Sunny",
        "forecast": [
            {"date": str(date.today() + timedelta(days=1)), "high": 20, "low": 14, "condition": "Sunny"},
            {"date": str(date.today() + timedelta(days=2)), "high": 22, "low": 15, "condition": "Clear"},
            {"date": str(date.today() + timedelta(days=3)), "high": 19, "low": 13, "condition": "Thunderstorms"},
            {"date": str(date.today() + timedelta(days=4)), "high": 17, "low": 11, "condition": "Rainy"},
            {"date": str(date.today() + timedelta(days=5)), "high": 21, "low": 14, "condition": "Partly Cloudy"},
        ],
    },
    "tokyo": {
        "temperature": 22.7,
        "condition": "Partly Cloudy",
        "forecast": [
            {"date": str(date.today() + timedelta(days=1)), "high": 24, "low": 18, "condition": "Sunny"},
            {"date": str(date.today() + timedelta(days=2)), "high": 25, "low": 19, "condition": "Clear"},
            {"date": str(date.today() + timedelta(days=3)), "high": 23, "low": 17, "condition": "Partly Cloudy"},
            {"date": str(date.today() + timedelta(days=4)), "high": 20, "low": 15, "condition": "Rainy"},
            {"date": str(date.today() + timedelta(days=5)), "high": 22, "low": 16, "condition": "Cloudy"},
        ],
    },
}


def get_city_data(city: str) -> dict:
    key = city.lower()
    if key not in WEATHER_DATA:
        available = ", ".join(c.title() for c in WEATHER_DATA)
        raise HTTPException(
            status_code=404,
            detail=f"City '{city}' not found. Available cities: {available}",
        )
    return WEATHER_DATA[key]


@app.get("/weather/temperature/{city}")
def get_temperature(city: str):
    """Returns the current temperature for a given city."""
    data = get_city_data(city)
    return {
        "city": city.title(),
        "temperature_celsius": data["temperature"],
        "condition": data["condition"],
    }


@app.get("/weather/forecast/{city}")
def get_forecast(city: str):
    """Returns the 5-day weather forecast for a given city."""
    data = get_city_data(city)
    return {
        "city": city.title(),
        "forecast": data["forecast"],
    }
