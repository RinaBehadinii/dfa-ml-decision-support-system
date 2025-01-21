from flask import Flask, render_template, request, jsonify

from modules.dfa import DFA
from modules.model import train_model, update_feedback
from modules.weather import get_weather, determine_weather_category

app = Flask(__name__)

# Load or Train Model
model = train_model()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    latitude, longitude = 41.6, 21.0
    weather_data = get_weather(latitude, longitude)

    if 'error' in weather_data:
        return jsonify({'outfit': None, 'status': weather_data['error']})

    weather_category = determine_weather_category(weather_data)
    print(f"Weather Category: {weather_category}")

    dfa = DFA()
    result = dfa.select_outfit(weather_category)

    if isinstance(result, list):
        return jsonify({
            'outfit': result,
            'status': 'Accepted',
            'weather': weather_data,
            'category': weather_category
        })
    else:
        return jsonify({'outfit': None, 'status': result})


@app.route('/feedback', methods=['POST'])
def feedback():
    top = request.form['top']
    bottom = request.form['bottom']
    outerwear = request.form['outerwear']
    user_feedback_response = request.form['feedback']

    update_feedback(top, bottom, outerwear, user_feedback_response)

    global model
    model = train_model()
    print("Model retrained successfully after feedback submission.")

    return "Feedback recorded and model retrained. Thank you!"


if __name__ == '__main__':
    app.run(debug=True)
