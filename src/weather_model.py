import re

from .weather_api import WeatherPlace, get_weather_city

def check_bad_weather(weather: WeatherPlace) -> str:
    level = 0
    if 0 <= weather.temperature <= 35:
        level += 1
    if weather.humidity < 70:
        level += 1
    if weather.speed_wind < 50:
        level += 1
    if weather.rain_probability < 80:
        level += 1
    
    levels = {
        0: 'Очень плохая погода!',
        1: 'Очень плохая погода!',
        2: 'Погода средняя, могло быть и лучше',
        3: 'Хорошая погода',
        4: 'Очень хорошая погода',
    }

    return levels.get(level)


def make_response(city_name: str) -> dict:
    resp = {
        'city_name': '',
        'latitude': '',
        'longitude': '',
        'weather': None,
        'status': '',
        'is_correct': None,
        }
    
    pattern = r"^[a-zA-Zа-яА-ЯёЁ]+$"

    if (not re.fullmatch(pattern, city_name)) or city_name == '' or city_name is None:
        resp['status'] = 'Упс. Неверно введён город или вы его не указали'
        resp['is_correct'] = False
        return resp

    weather = get_weather_city(city_name=city_name)
    if not weather:
        resp['status'] = 'Данные недоступны, ошибка API'
        resp['is_correct'] = False
        return resp

    about_weather = check_bad_weather(weather)

    resp['city_name'] = city_name
    resp['status'] = about_weather
    resp['latitude'] = weather.latitude
    resp['longitude'] = weather.longitude
    resp['weather'] = weather
    resp['is_correct'] = True

    return resp
