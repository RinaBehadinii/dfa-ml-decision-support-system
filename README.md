## README

### Project Overview
This project is a web-based outfit recommendation system using a Deterministic Finite Automaton (DFA). The system provides weather-responsive, constraint-based outfit suggestions and adapts recommendations based on user feedback.

### Features
- **Weather-Responsive Recommendations:** Fetches real-time weather data and categorizes it.
- **DFA Validation:** Ensures outfits follow a logical sequence (`Top -> Bottom -> Outerwear`).
- **Feedback-Based Personalization:** Uses user feedback to improve recommendations.
- **Color and Category Constraints:** Enforces a maximum of three distinct colors and mandatory categories based on weather.

### Setup
1. Install dependencies: `pip install -r requirements.txt`.
2. Place the `wardrobe.csv` file in the `data/` directory.
3. Run the app: `python app.py`.
4. Open `http://127.0.0.1:5000` in your browser.

### Usage
1. View the current weather and get outfit recommendations.
2. Provide feedback (like/dislike) to improve suggestions.
3. The system adapts to preferences over time.
