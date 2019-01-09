from flask import Flask, render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
import requests
from forecastiopy import *

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(50), nullable=True, unique=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)


@app.route('/', methods=['GET', 'POST'])
#@app.route('/')
def index():
    if request.method == 'POST':
         new_city = request.form.get('city')
         lat = request.form.get("latitude")
         long = request.form.get('longitude')
         print(new_city + str(lat) + str(long))
         if new_city and lat and long:
             new_city_obj = City(city=new_city, latitude=lat, longitude=long)
             db.session.add(new_city_obj)
             db.session.commit()
    cities = City.query.all()

    apikey = {}
    weather_data = []

    atl = [33.7490, -84.3880] #just for testing purposes
    for city in cities:
        fio = ForecastIO.ForecastIO(apikey, latitude=city.latitude, longitude=city.longitude)
        current = FIOCurrently.FIOCurrently(fio)

        daily = current
        hourly = current

        if fio.has_daily() is True:
            daily = FIODaily.FIODaily(fio)

        if fio.has_hourly() is True:
            hourly = FIOHourly.FIOHourly(fio)

        iconstring = current.icon.upper().replace("-", "_")
        weather = {
            'city': city.city,
            'temperature': current.temperature,
            'description': hourly.summary,
            'icon': iconstring,  # need to try all 10
        }
        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)
