from enum import Enum

API_URL = "https://api.open-meteo.com/v1/forecast"
CSV_FILE = 'data/wardrobe.csv'
FEEDBACK_FILE = 'data/feedback.csv'

user_feedback = {}


class WeatherCategory(Enum):
    SNOWY = "Snowy"
    COLD = "Cold"
    RAINY = "Rainy"
    MODERATE = "Moderate"
    HOT = "Hot"
