# Hersh Rudrawal
# weather.py
# Contains functions required to update
# the database with weather data
# Also contains the page routes to display
# the data in db
# Contains API to query db
import os
import xmltodict
import json
import requests
import datetime
import csv

from flask import (
    current_app, Blueprint, flash, redirect, render_template, request,url_for
)

from werkzeug.exceptions import abort
from .extensions import db
from .models import OwmCities, OwmCurrentWeather, OwmHourlyWeatherForecast

bp = Blueprint('weather', __name__)

# Add your own Open Weather Api Key here
owm_api_key = current_app.config['OPENWEATHERMAP_API_KEY']

# location of directory storing historical data
historical_data_path = current_app.config["WEATHER_DATA_PATH"]


# function to return a list of city ids
def city_ids():
    result = OwmCities.query.with_entities(OwmCities.city_id)
    id = [r for (r,) in result]
    return id


def add_city(latitude, longitude):
    error = None
    if latitude is None or longitude is None:
        print('Add City Error: Latitude or Longitude is missing')
        return

    url = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}".format(lat=latitude, lon=longitude, key=owm_api_key)
    r = requests.get(url)
    if r.status_code != 200:
        print('Add City Error: Request failed Status code: ' + str(r.status_code))
        print('Can not get data for city at {}, {}'.format(latitude, longitude))
    else:
        data = r.json()
        city = OwmCities.query.filter_by(city_id=data['id']).first()
        if city is None:
            city = OwmCities(city_id=data['id'],
                             city_name=data['name'],
                             city_coord_long=data['coord']['lon'],
                             city_coord_lat=data['coord']['lat'],
                             city_country=data['sys']['country']
                             )
            db.session.add(city)
            db.session.commit()
        return city.city_id


# will get the current weather for a given city
# and updated owm_current_weather with the data
# able to call with free api key
def update_current_weather(city_id):
    error = None

    # check is city is being tracked
    city = OwmCities.query.filter_by(city_id=city_id).first()
    if city is None:
        abort(404, f"City id {city_id} doesn't exist.")
    latitude = city.city_coord_lat
    longitude = city.city_coord_long
    if latitude is None or longitude is None:
        error = 'Update Current Weather Error: coordinates missing for city: ' + str(city_id)

    if error is None:
        timestamp = datetime.datetime.utcnow().replace(microsecond=0)

        # get weather data in xml format
        url = "https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={key}&units=metric&mode=xml".format(
            lat=latitude, lon=longitude, key=owm_api_key)
        r = requests.get(url)
        if r.status_code == 200:
            # convert xml format to dictionary
            data = xmltodict.parse(r.content, attr_prefix="")['current']

            # convert timestamps to datetime
            sunrise = datetime.datetime.strptime(data['city']['sun']['rise'], "%Y-%m-%dT%H:%M:%S")
            sunset = datetime.datetime.strptime(data['city']['sun']['set'], "%Y-%m-%dT%H:%M:%S")
            lastupdate_value = datetime.datetime.strptime(data['lastupdate']['value'], "%Y-%m-%dT%H:%M:%S")

            # check for wind
            if data['wind']['direction'] is None:
                wind_direction_value_deg = None
                wind_direction_code = None
                wind_direction_name = None
            else:
                wind_direction_value_deg = data['wind']['direction']['value']
                wind_direction_code = data['wind']['direction']['code']
                wind_direction_name = data['wind']['direction']['name']

            # insert data into owm_current_weather
            weather = OwmCurrentWeather(city_id=city_id,
                                        city_sun_rise=sunrise,
                                        city_sun_set=sunset,
                                        timezone_offset=data['city']['timezone'],
                                        timestamp=timestamp,
                                        lastupdate_value=lastupdate_value,
                                        temperature_value=data['temperature']['value'],
                                        temperature_min=data['temperature']['min'],
                                        temperature_max=data['temperature']['max'],
                                        temperature_unit=data['temperature']['unit'],
                                        feels_like_value=data['feels_like']['value'],
                                        feels_like_unit=data['feels_like']['unit'],
                                        humidity_value=data['humidity']['value'],
                                        pressure_value=data['pressure']['value'],
                                        wind_speed_value=data['wind']['speed']['value'],
                                        wind_speed_name=data['wind']['speed']['name'],
                                        wind_direction_value_deg=wind_direction_value_deg,
                                        wind_direction_code=wind_direction_code,
                                        wind_direction_name=wind_direction_name,
                                        cloud_value_pct=data['clouds']['value'],
                                        cloud_name=data['clouds']['name'],
                                        visibility_value_m=data['visibility']['value'],
                                        precipitation_value_mm=0 if 'value' not in data['precipitation'] else
                                        data['precipitation']['value'],
                                        precipitation_mode=data['precipitation']['mode'],
                                        weather_number=data['weather']['number'],
                                        weather_value=data['weather']['value'],
                                        weather_icon=data['weather']['icon']
                                        )
            db.session.add(weather)
            db.session.commit()
        else:
            error = 'Update Current Weather Error: {} Failed to connect to Open Weather API\nstatus code: {}'.format(city_id, r.status_code)
    if error is not None:
        print(error)
    return


# will give forecast for a city,
# in 3h intervals
# if days is 1, will get the next 24hours forecast
# able to call with free api key
def update_forcast_3h(city_id, days=5):
    # ensure days is within range
    if days < 1:
        days = 1
    if days > 5:
        days = 5
    timestamps = days * 8  # number of timestamps to receive from api call, 8 timestamps per day

    error = None

    # check is city is being tracked
    city = OwmCities.query.filter_by(city_id=city_id).first()
    if city is None:
        abort(404, f"City id {city_id} doesn't exist.")

    latitude = city.city_coord_lat
    longitude = city.city_coord_long
    if latitude is None or longitude is None:
        error = 'Update Weather Hourly Error: coordinates missing for city: ' + str(city_id)
    if error is None:
        url = 'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&cnt={count}&appid={key}&mode=xml'.format(
            lat=latitude, lon=longitude, count=timestamps, key=owm_api_key)
        r = requests.get(url)
        if r.status_code == 200:
            # convert to dictionary
            data = xmltodict.parse(r.content, attr_prefix="")['weatherdata']

            request_timestamp = datetime.datetime.utcnow().replace(microsecond=0)
            for i in range(0, timestamps):
                # convert timestamps to datetime
                sunrise = datetime.datetime.strptime(data['sun']['rise'], "%Y-%m-%dT%H:%M:%S")
                sunset = datetime.datetime.strptime(data['sun']['set'], "%Y-%m-%dT%H:%M:%S")
                forecast_timestamp = datetime.datetime.strptime(data['forecast']['time'][i]['to'],
                                                                "%Y-%m-%dT%H:%M:%S").replace(microsecond=0)
                lastupdate_value = None
                if data['meta']['lastupdate'] is not None:
                    lastupdate_value = datetime.datetime.strptime(data['meta']['lastupdate'], "%Y-%m-%dT%H:%M:%S")

                # check if there is no wind
                if data['forecast']['time'][i]['windDirection'] is None:
                    wind_direction_value_deg = None
                    wind_direction_code = None
                    wind_direction_name = None
                else:
                    wind_direction_value_deg = data['forecast']['time'][i]['windDirection']['deg']
                    wind_direction_code = data['forecast']['time'][i]['windDirection']['code']
                    wind_direction_name = data['forecast']['time'][i]['windDirection']['name']


                weather = OwmHourlyWeatherForecast(forecast_timestamp=forecast_timestamp,
                                                   city_id=city_id,
                                                   city_sun_rise=sunrise,
                                                   city_sun_set=sunset,
                                                   timezone_offset=data['location']['timezone'],
                                                   request_timestamp=request_timestamp,
                                                   lastupdate_value=lastupdate_value,
                                                   temperature_value=data['forecast']['time'][i]['temperature'][
                                                       'value'],
                                                   temperature_min=data['forecast']['time'][i]['temperature']['min'],
                                                   temperature_max=data['forecast']['time'][i]['temperature']['max'],
                                                   temperature_unit=data['forecast']['time'][i]['temperature']['unit'],
                                                   feels_like_value=data['forecast']['time'][i]['feels_like']['value'],
                                                   feels_like_unit=data['forecast']['time'][i]['feels_like']['unit'],
                                                   humidity_value=data['forecast']['time'][i]['humidity']['value'],
                                                   pressure_value=data['forecast']['time'][i]['pressure']['value'],
                                                   wind_speed_value=data['forecast']['time'][i]['windSpeed']['mps'],
                                                   wind_speed_name=data['forecast']['time'][i]['windSpeed']['name'],
                                                   wind_direction_value_deg=wind_direction_value_deg,
                                                   wind_direction_code=wind_direction_code,
                                                   wind_direction_name=wind_direction_name,
                                                   cloud_value_pct=data['forecast']['time'][i]['clouds']['all'],
                                                   cloud_name=data['forecast']['time'][i]['clouds']['value'],
                                                   visibility_value_m=data['forecast']['time'][i]['visibility'][
                                                       'value'],
                                                   precipitation_value_mm=0 if 'value' not in
                                                                               data['forecast']['time'][i][
                                                                                   'precipitation'] else
                                                   data['forecast']['time'][i]['precipitation']['value'],
                                                   precipitation_mode='no' if 'type' not in data['forecast']['time'][i][
                                                       'precipitation'] else
                                                   data['forecast']['time'][i]['precipitation']['type'],
                                                   weather_number=data['forecast']['time'][i]['symbol']['number'],
                                                   weather_value=data['forecast']['time'][i]['symbol']['name'],
                                                   weather_icon=data['forecast']['time'][i]['symbol']['var']
                                                   )
                db.session.add(weather)
            db.session.commit()
        else:
            error = 'Update Current Weather Error: {} Failed to connect to Open Weather API\nstatus code: {}'.format(city_id, r.status_code)
    if error is not None:
        print(error)
    return


# reads a csv file containing historical weather data for a city
# and updated owm_current_weather table with data
# does not override existing data, as csv
# does not contain all required data fields
def weather_import(filename):
    '''
        Data provided in CSV file
        dt, timezone, temp, visiblity
        feels like temp, temp min, temp max
        pressure, humidity, windspeed
        wind deg, rain 1h or snow 1h, mode: no, rain, snow,
        weather id, weather desc., weather icon
    '''
    error = None
    if filename is None:
        error = "No file to read"
    else:
        with open(filename) as csv_file:
            data = csv.DictReader(csv_file)
            first_line = next(data)
            exists = db.session.query(OwmCities) \
                .filter_by(city_name=first_line["city_name"]) \
                .first()

            if exists is None:
                print('add new city')
                city_id = add_city(float(first_line['lat']), float(first_line['lon']))
            else:
                print('city exists')
                city_id = exists.city_id

            for line in data:
                timestamp = datetime.datetime.utcfromtimestamp(int(line['dt']))
                entry = db.session.query(OwmCurrentWeather).filter_by(city_id=city_id, timestamp=timestamp).first()
                if entry is not None:
                    continue

                if line['visibility']:
                    visibility_value_m = int(line['visibility'])
                else:
                    visibility_value_m = None

                if line['rain_1h']:
                    precipitation_value_mm = float(line['rain_1h'])
                    precipitation_mode = 'rain'
                elif line['snow_1h']:
                    precipitation_value_mm = float(line['snow_1h'])
                    precipitation_mode = 'snow'
                else:
                    precipitation_value_mm = 0
                    precipitation_mode = 'no'

                #temp = round(float(line['temp']), 2)
                #temp_min = round(float(line['temp_min']), 2)
                #temp_max = round(float(line['temp_max']), 2)
                #feels_like = round(float(line['feels_like']), 2)
                weather = OwmCurrentWeather(city_id=city_id,
                                            timezone_offset=int(line['timezone']),
                                            timestamp=timestamp,
                                            temperature_value=float(line['temp']),
                                            temperature_min=float(line['temp_min']),
                                            temperature_max=float(line['temp_max']),
                                            feels_like_value=float(line['feels_like']),
                                            humidity_value=int(line['humidity']),
                                            pressure_value=int(line['pressure']),
                                            wind_speed_value=float(line['wind_speed']),
                                            wind_direction_value_deg=int(line['wind_deg']),
                                            visibility_value_m=visibility_value_m,
                                            precipitation_value_mm=float(precipitation_value_mm),
                                            precipitation_mode=precipitation_mode,
                                            weather_number=int(line['weather_id']),
                                            weather_value=line['weather_description'],
                                            weather_icon=line['weather_icon']
                                            )
                db.session.add(weather)
            db.session.commit()
    if error is not None:
        print(error)
    return


# Routes

# updates the current weather to owm_current_weather for given city
@bp.route('/weather/<int:city_id>/current', methods=('GET', 'POST'))
def current_weather(city_id):
    # error = update_current_weather_all()
    city = db.session.query(OwmCities) \
        .filter_by(city_id=city_id) \
        .first()
    if city is None:
        abort(404, f"City id {city_id} doesn't exist.")

    data = db.session.query(OwmCurrentWeather) \
        .order_by(OwmCurrentWeather.timestamp.desc()) \
        .filter_by(city_id=city_id) \
        .all()

    return render_template('weather/currentweather.html', city=city, data=data)


# updates the current forcast to owm_hourly_weather_forecast for given city
@bp.route('/weather/<int:city_id>/forecast', methods=('GET', 'POST'))
def current_forecast(city_id):
    city = db.session.query(OwmCities) \
        .filter_by(city_id=city_id) \
        .first()
    if city is None:
        abort(404, f"City id {city_id} doesn't exist.")
    data = db.session.query(OwmHourlyWeatherForecast) \
        .order_by(OwmHourlyWeatherForecast.forecast_timestamp.asc()) \
        .filter_by(city_id=city_id) \
        .all()
    return render_template('weather/currentforecast.html', city=city, data=data)


@bp.route('/weather/remove/<int:city_id>', methods=('GET', 'POST'))
def remove_city(city_id):
    city = OwmCities.query.filter_by(city_id=city_id).first()
    if city is None:
        abort(404, f"City id {city_id} doesn't exist.")
    db.session.query(OwmCurrentWeather).filter_by(city_id=city_id).delete()
    db.session.query(OwmHourlyWeatherForecast).filter_by(city_id=city_id).delete()
    db.session.delete(city)
    db.session.commit()
    return redirect(url_for('cities.index'))


# todo find reliable way to convert sqlalchemy results to json

def row2dict(row):
    if row is None:
        return
    d = {}
    for column in row.__table__.columns:
        if isinstance(column, datetime.date):
            d[column.name] = column.isoformat()
        else:
            d[column.name] = str(getattr(row, column.name))
    return d


# returns all data in owm_current_weather for a given city as a json
@bp.route('/weather/<int:city_id>/current/dump', methods=('GET', 'POST'))
def current_weather_dump(city_id):
    # {city info, weather entries, weather data}
    city = OwmCities.query.filter_by(city_id=city_id).first()
    if city is None:
        abort(404, f"City id {city_id} doesn't exist.")

    data = OwmCurrentWeather.query \
        .filter_by(city_id=city_id) \
        .order_by(OwmCurrentWeather.timestamp.asc())

    weather = {"city": row2dict(city), "count": data.count(), "data": []}
    for d in data.all():
        entry = row2dict(d)
        entry.pop('id')
        entry.pop('city_id')
        weather['data'].append(entry)
    return json.dumps(weather)


# returns all data in owm_hourly_weather_forecast for a given city as a json
@bp.route('/weather/<int:city_id>/forecast/dump', methods=('GET', 'POST'))
def forecast_dump(city_id):
    # {city info, weather entries, weather data}
    city = OwmCities.query.filter_by(city_id=city_id).first()
    if city is None:
        abort(404, f"City id {city_id} doesn't exist.")

    data = OwmHourlyWeatherForecast.query \
        .filter_by(city_id=city_id) \
        .order_by(OwmHourlyWeatherForecast.forecast_timestamp.asc())

    weather = {"city": row2dict(city), "count": data.count(), "data": []}

    for d in data.all():
        entry = row2dict(d)
        entry.pop('id')
        entry.pop('city_id')
        weather['data'].append(entry)
    return json.dumps(weather)


@bp.route('/weather/import/<int:city_id>', methods=('GET', 'POST'))
def import_data(city_id):
    city = OwmCities.query.filter_by(city_id=city_id).first()
    if city is None:
        abort(404, f"City id {city_id} doesn't exist.")
    for filename in os.listdir(historical_data_path):
        f = os.path.join(historical_data_path, filename)
        if os.path.isfile(f) and f.endswith('.csv'):
            if city.city_name.lower() in f:
                weather_import(f)
                flash("Imported data for " + city.city_name)
                return redirect(url_for('cities.index'))
    flash("No file to import data for " + city.city_name)
    return redirect((url_for('cities.index')))


@bp.route('/weather/import/all', methods=('GET', 'POST'))
def import_all():
    flash("Importing")
    for filename in os.listdir(historical_data_path):
        f = os.path.join(historical_data_path, filename)
        if os.path.isfile(f) and f.endswith('.csv'):
            print('import' + f)
            weather_import(f)
    flash("Imported all data")
    return redirect(url_for('cities.index'))


'API CALLS'
#returns all the cities and their location data
# {city_name:{city_id,city_name,city_coord_lat,city_coord_long,city_country},...}
@bp.route('/get_location_data')
def get_city_data():
    cities = OwmCities.query.all()
    data = dict()
    for c in cities:
        row = row2dict(c)
        data[row['city_name']] = row
    return json.dumps(data)


#returns all the cities and their corresponding ids
#format: /get_location_ids
@bp.route('/get_location_ids')
def get_city_ids():
    cities = OwmCities.query.all()
    data = dict()
    for c in cities:
        row = (row2dict(c))
        data[row['city_name']] = row['city_id']
    return json.dumps(data)


#get city id based on lat,long coordinate
#format: /get_location_id?lat=<latitude>&long=<longitude>
@bp.route('/get_location_id')
def get_city_id():
    latitude = request.args.get('lat', type=float)
    longitude = request.args.get('long', type=float)
    city = OwmCities.query.filter_by(city_coord_lat=latitude, city_coord_long=longitude).first()
    if city is None:
        url = "http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit={limit}&appid={key}" \
            .format(lat=latitude, lon=longitude, limit=1, key=owm_api_key)
        r = requests.get(url)
        if r.status_code != 200:
            abort(404, 'Cannot find city or weather station for {}, {}'.format(latitude, longitude))
        else:
            data = r.json()
            if not data:
                abort(404, 'Cannot find city or weather station for {}, {}'.format(latitude, longitude))
            name = data[0]['name']
            name = name.replace("City of ", "")
            city = OwmCities.query.filter_by(city_name=name, city_country=data[0]['country']).first()
            if city is None:
                abort(404, 'Not tracking weather for location at {}, {}'.format(latitude, longitude))
    return json.dumps(city.city_id)

# returns the weather for a city at a given time
# format /get_weather_by_date?id=<location id>&date=<iso-8601 utc timestamp>
@bp.route('/get_weather_by_date', methods=('GET', 'POST'))
def get_weather_by_date():
    city_id = request.args.get('id', type=int)
    date = request.args.get('date')
    dt = datetime.datetime.fromisoformat(date)
    weather = {'type': 'current', 'is_found': True}
    data = OwmCurrentWeather.query \
        .filter_by(city_id=city_id, timestamp=date).first()

    if data is None:
        weather['is_found'] = False
        # limit search to entire day
        dtrange = dt.replace(hour=23, minute=59, second=59)

        # find closest current
        current = row2dict(OwmCurrentWeather.query
                           .filter(OwmCurrentWeather.city_id == city_id,
                                   OwmCurrentWeather.timestamp >= dt,
                                   OwmCurrentWeather.timestamp <= dtrange)
                           .order_by(OwmCurrentWeather.timestamp.asc()).first())

        #find closest forcast
        forecast = row2dict(OwmHourlyWeatherForecast.query
                            .filter(OwmHourlyWeatherForecast.city_id == city_id,
                                    OwmHourlyWeatherForecast.forecast_timestamp >= dt,
                                    OwmHourlyWeatherForecast.forecast_timestamp <= dtrange)
                            .order_by(OwmHourlyWeatherForecast.forecast_timestamp.asc(),
                                      OwmHourlyWeatherForecast.request_timestamp.desc()).first())

        if forecast is None and current is None:
            return json.dumps(dict())
        if forecast is not None and current is None:
            weather['type'] = 'forecast'
            row = forecast
        elif forecast is None and current is not None:
            row = current
        elif current['timestamp'] > forecast['forecast_timestamp']:
            weather['type'] = 'forecast'
            row = forecast
        else:
            row = current
    else:
        row = row2dict(data)
    row.pop('id')
    return json.dumps(weather | row)

