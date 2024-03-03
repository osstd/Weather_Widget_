from flask import Flask, render_template, request, flash, redirect, url_for
import requests
import pycountry
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('F_KEY')
API_KEY = os.environ.get('API_KEY')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        c_code = False

        if 'c' in request.form:
            units = 'metric'
        else:
            units = 'imperial'
        parameters = {
            "units": units,
            "appid": API_KEY,
            "lang": "en",
        }

        location = request.form['city']
        if location == "":
            flash("Please input a city name first!")
            return redirect(url_for('home'))
        if ',' in location:
            parts = location.split(",")
            city = parts[0].strip()
            if len(parts) > 1:
                country = parts[1].strip()
                if country:
                    try:
                        c_code = pycountry.countries.lookup(country).alpha_2
                    except LookupError:
                        c_code = None
        else:
            city = location.strip()
        try:
            if c_code and c_code is not None:
                response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city},{c_code}",
                                        params=parameters)
                response.raise_for_status()
            else:
                response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}",
                params=parameters)
                response.raise_for_status()
            weather_data = response.json()
            return render_template('index.html', display='true', data=weather_data, units=units)
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            flash("Invalid city name!")
            return redirect(url_for('home'))
        except Exception as err:
            return f'{err}'
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False)
