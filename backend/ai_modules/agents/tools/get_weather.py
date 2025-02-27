from typing import Annotated, List, Optional, Union, Literal
from pydantic import BaseModel
from backend.utils.tool_wrapper import tool
import os
import requests

class WeatherForecast(BaseModel):
    date: Optional[str]
    max_temp: Optional[Union[float, str]]
    min_temp: Optional[Union[float, str]]
    chance_of_rain: Optional[Union[float, str]]
    air_quality: Optional[Union[str, int]]
    humidity: Optional[Union[float, str]]
    condition: Optional[str]
    
class CurrentWeather(BaseModel):
    date: Optional[str]
    temp: Optional[Union[float, str]]
    chance_of_rain: Optional[Union[float, str]]
    air_quality: Optional[Union[str, int]]
    humidity: Optional[Union[float, str]]
    condition: Optional[str]
    
class WeatherResponse(BaseModel):
    location: Optional[str]
    current_weather: Optional[CurrentWeather]
    forecast: Optional[List[WeatherForecast]]

@tool(
    description="Get the weather forecast for a location. If no location is provided, the location will automatically be determined using the IP address.",
)
def get_weather(
    mode: Annotated[Literal["current", "forecast", "both"], "Weather Response mode."],
    location: Annotated[Union[str, Literal["Unknown"]], "The location to get the weather forecast for."], 
    days: Annotated[Union[int, Literal["Unknown"]], "The number of days to get the weather forecast for. Maximum of 3"] = 3,
    ) -> List[Union[str, int]]:
    weather_api_key = os.getenv("WEATHERAPI_API_KEY")
    if weather_api_key is None:
        raise ValueError("Weather API key not found.")
    
    # Add one more day because the first forecast is for the current day
    days += 1
    
    def get_location():
        try:
            response = requests.get('https://ipinfo.io')
            data = response.json()
            city = data.get('city', 'Unknown')
            return city
        except:
            print("Internet Not avialable")
            exit()
            return False
    
    if location == "Unknown":
        location = get_location()
    
    weather = requests.get(f"https://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={location}&days={days}&aqi=yes&alerts=yes")   
    
    if weather.status_code != 200:
        raise ValueError(f"Failed to fetch weather data: {weather.json().get('error', 'Unknown error')}")
    
    weather_data = weather.json()
    
    current_data = weather_data["current"]
    current_weather = CurrentWeather(
        date=current_data.get("last_updated"),
        temp=current_data.get("temp_c"),
        chance_of_rain=weather_data["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"],
        air_quality=current_data.get("air_quality").get("us-epa-index", "Unknown"),
        humidity=current_data.get("humidity"),
        condition=current_data.get("condition")["text"]
    ).model_dump()
    
    forecasts = weather_data["forecast"]["forecastday"]
    
    forecasts_response = []
    
    for forecast in forecasts[1:]:
        forecast_details = WeatherForecast(
            date=forecast["date"],
            max_temp=forecast["day"]["maxtemp_c"],
            min_temp=forecast["day"]["mintemp_c"],
            chance_of_rain=forecast["day"]["daily_chance_of_rain"],
            air_quality=forecast["day"]["air_quality"].get("us-epa-index", "Unknown"),
            humidity=forecast["day"]["avghumidity"],
            condition=forecast["day"]["condition"]["text"]
        )
        forecasts_response.append(forecast_details.model_dump())
    
    weather_response = WeatherResponse(
        location=location,
        current_weather=current_weather if mode in ["both", "current"] else None,
        forecast=forecasts_response if mode in ["both", "forecast"] else None
    ).model_dump()
    
    return weather_response