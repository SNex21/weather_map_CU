import requests
from dataclasses import dataclass


from config import api_key


@dataclass
class WeatherPlace:
    def __init__(
            self, 
            temperature: float, 
            humidity: float, 
            speed_wind: float, 
            rain_probability: float,
            ) -> None:
        self.temperature = temperature
        self.humidity = humidity
        self.speed_wind = speed_wind
        self.rain_probability = rain_probability


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
            location_key = location.get('Key', None)
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
            temperature = weather.get('Temperature', None).get('Value', None)
            humidity = weather.get('RelativeHumidity', None)
            speed_wind = weather.get('Wind', None).get('Speed', None).get('Value', None)
            rain_probability = weather.get('RainProbability', None)
            
            return WeatherPlace(
                temperature=temperature, 
                humidity=humidity,
                speed_wind=speed_wind,
                rain_probability=rain_probability,
            )

        raise f'{response.status_code} | {response.text}'
    except Exception as e:
        print(e)
        return None
