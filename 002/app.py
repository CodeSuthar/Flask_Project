from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/getweather', methods=['POST'])
def get_weather():
    city = request.form['city']

    # Fetch GEOCODING DATA
    geocoding_url = f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=10&language=en&format=json'
    geocoding_response = requests.get(geocoding_url)
    geocoding_data = geocoding_response.json()

    if 'results' in geocoding_data and len(geocoding_data['results']) > 0:
        latitude = geocoding_data['results'][0]['latitude']
        longitude = geocoding_data['results'][0]['longitude']

        # Fetch WEATHER DATA
        weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true'
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if 'current_weather' in weather_data:
            print(weather_data)
            return render_template('index.html', weather=weather_data['current_weather'], units=weather_data['current_weather_units'], city=city)
        else:
            error_message = f"Weather data for '{city}' is not available at the moment."
            return render_template('index.html', error=error_message)
    else:
        error_message = f"City '{city}' not found. Please enter a valid city name."
        return render_template('index.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)