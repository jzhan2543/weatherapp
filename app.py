from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import request
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
    # if request.method == 'POST':
    #      new_city = request.form.get('city')
    #      lat = request.form.get("latitude")
    #      long = request.form.get('longitude')
    #      if new_city and lat and long:
    #          new_city_obj = City(city=new_city, latitude=lat, longitdue=long)
    #          db.session.add(new_city_obj)
    #          db.session.commit()
    cities = City.query.all()

    apikey = '0aeec00f1b38da64c35ee0583f943ed8'
    weather_data = []

    atl = [33.7490, -84.3880]
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