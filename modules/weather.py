import requests

from modules.constants import API_URL, WeatherCategory


def get_weather(latitude, longitude):
    url = f"{API_URL}?latitude={latitude}&longitude={longitude}&current_weather=true"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('current_weather', {})
        else:
            return {"error": "Unable to fetch weather data."}
    except Exception as e:
        return {"error": str(e)}


def determine_weather_category(weather_data):
    temperature = weather_data.get('temperature', 0)
    weather_code = weather_data.get('weathercode', 0)

    weather_code_map = {
        range(61, 68): WeatherCategory.RAINY,
        range(71, 76): WeatherCategory.SNOWY,
        range(95, 100): WeatherCategory.RAINY,
    }

    if temperature < 5:
        category = WeatherCategory.SNOWY
    elif temperature < 15:
        category = WeatherCategory.COLD
    elif temperature > 25:
        category = WeatherCategory.HOT
    else:
        category = WeatherCategory.MODERATE

    for code_range, mapped_category in weather_code_map.items():
        if weather_code in code_range:
            category = mapped_category
            break

    return category.value
