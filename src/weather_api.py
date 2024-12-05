import requests
from dataclasses import dataclass

from .config import api_key


@dataclass
class WeatherPlace:
    def __init__(
            self, 
            temperature: float, 
            humidity: float, 
            speed_wind: float, 
            rain_probability: float,
            latitude: float,
            longitude: float,
            ) -> None:
        self.temperature = temperature
        self.humidity = humidity
        self.speed_wind = speed_wind
        self.rain_probability = rain_probability
        self.latitude = latitude
        self.longitude = longitude


def detect_language(input_text: str) -> str:
    if all("а" <= char <= "я" or char == "ё" for char in input_text.lower() if char.isalpha()):
        return "ru-ru"
    return "en-us"


def get_weather_coords(latitude: float, longitude: float) -> WeatherPlace | None:
    try:
        request_url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
        query = {
            'apikey': api_key,
            'q': f'{latitude},{longitude}',
            'language': 'en-us',
            'details': False,
            'toplevel':False,

        }

        response = requests.get(url=request_url, params=query)

        if response.status_code == 200:
            location: dict = response.json()
            location_key = location.get('Key')
            if not location_key:
                return None
        else:
            raise f'{response.status_code} | {response.text}'
    except Exception as e:
        print(e)
        return None
    
    try:
        request_url = f'http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{location_key}'
        query = {
            'apikey': api_key,
            'language': 'en-us',
            'details': True,
            'metric': True,
        }

        response = requests.get(url=request_url, params=query)

        if response.status_code == 200:
            weather: dict = response.json()[0]
            temperature = weather.get('Temperature').get('Value')
            humidity = weather.get('RelativeHumidity')
            speed_wind = weather.get('Wind').get('Speed').get('Value')
            rain_probability = weather.get('RainProbability')
            
            return WeatherPlace(
                temperature=temperature, 
                humidity=humidity,
                speed_wind=speed_wind,
                rain_probability=rain_probability,
                latitude=latitude,
                longitude=longitude,
            )

        raise f'{response.status_code} | {response.text}'
    except Exception as e:
        print(e)
        return None
    

def get_weather_city(city_name: str) -> WeatherPlace | None:
    lan = detect_language(city_name)
    try:
        request_url = 'http://dataservice.accuweather.com/locations/v1/cities/search'
        query = {
            'apikey': api_key,
            'q': city_name,
            'language': lan,
            'details': True,
            'toplevel':False,

        }
        response = requests.get(url=request_url, params=query)

        if response.status_code == 200:
            location: dict = response.json()[0]
            location_key = location.get('Key')

            latitude=location.get('GeoPosition').get('Latitude')
            longitude=location.get('GeoPosition').get('Longitude')

        else:
            raise f''
    except Exception as e:
        print(e ,'|',  f'{response.status_code} | {response.text}')
        return None
    
    try:
        request_url = f'http://dataservice.accuweather.com/forecasts/v1/hourly/1hour/{location_key}'
        query = {
            'apikey': api_key,
            'language': 'en-us',
            'details': True,
            'metric': True,
        }

        response = requests.get(url=request_url, params=query)

        if response.status_code == 200:
            weather: dict = response.json()[0]
            temperature = weather.get('Temperature').get('Value')
            humidity = weather.get('RelativeHumidity')
            speed_wind = weather.get('Wind').get('Speed').get('Value')
            rain_probability = weather.get('RainProbability')
            
            return WeatherPlace(
                temperature=temperature, 
                humidity=humidity,
                speed_wind=speed_wind,
                rain_probability=rain_probability,
                latitude=latitude,
                longitude=longitude,
            )

        raise ''
    except Exception as e:
        print(e ,'|', f'{response.status_code} | {response.text}')
        return None
