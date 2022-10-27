from .extensions import db
import datetime


class OwmCities(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'owm_cities'
    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(), nullable=False)
    city_coord_lat = db.Column(db.Float, nullable=False)
    city_coord_long = db.Column(db.Float, nullable=False)
    city_country = db.Column(db.String(), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class OwmCurrentWeather(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'owm_current_weather'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=(datetime.datetime.utcnow()).replace(microsecond=0))
    city_id = db.Column(db.Integer, db.ForeignKey("owm_cities.city_id"), nullable=False)
    city_sun_rise = db.Column(db.DateTime, nullable=True)
    city_sun_set = db.Column(db.DateTime, nullable=True)
    timezone_offset = db.Column(db.Integer, nullable=False)
    temperature_value = db.Column(db.Float, nullable=False)
    temperature_min = db.Column(db.Float, nullable=False)
    temperature_max = db.Column(db.Float, nullable=False)
    temperature_unit = db.Column(db.String(), default='celsius', nullable=False)
    feels_like_value = db.Column(db.Float, nullable=False)
    feels_like_unit = db.Column(db.String(), default='celsius', nullable=False)
    humidity_value = db.Column(db.Integer, nullable=False)
    humidity_unit = db.Column(db.String(), default='%', nullable=False)
    pressure_value = db.Column(db.Integer, nullable=False)
    pressure_unit = db.Column(db.String(), default='hPa', nullable=False)
    wind_speed_value = db.Column(db.Float, nullable=False)
    wind_speed_unit = db.Column(db.String(), default='m/s', nullable=False)
    wind_speed_name = db.Column(db.String(), nullable=True)
    wind_direction_value_deg = db.Column(db.Integer, nullable=True)
    wind_direction_code = db.Column(db.String(), nullable=True)
    wind_direction_name = db.Column(db.String(), nullable=True)
    cloud_value_pct = db.Column(db.Float, nullable=True)
    cloud_name = db.Column(db.String(), nullable=True)
    visibility_value_m = db.Column(db.Integer, nullable=True)
    precipitation_value_mm = db.Column(db.Float, default=0.0, nullable=False)
    precipitation_mode = db.Column(db.String(), default='no', nullable=False)
    weather_number = db.Column(db.Integer, nullable=False)
    weather_value = db.Column(db.String(), nullable=False)
    weather_icon = db.Column(db.String(), nullable=False)
    lastupdate_value = db.Column(db.DateTime, nullable=True)


class OwmHourlyWeatherForecast(db.Model):
    __table_args__ = {'extend_existing': True}
    __tablename__ = 'owm_hourly_weather_forecast'
    id = db.Column(db.Integer, primary_key=True)
    request_timestamp = db.Column(db.DateTime,  nullable=False, default=datetime.datetime.utcnow())
    forecast_timestamp = db.Column(db.DateTime, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey("owm_cities.city_id"), nullable=False)
    city_sun_rise = db.Column(db.DateTime, nullable=False)
    city_sun_set = db.Column(db.DateTime, nullable=False)
    timezone_offset = db.Column(db.Integer, nullable=False)
    temperature_value = db.Column(db.Float, nullable=False)
    temperature_min = db.Column(db.Float, nullable=False)
    temperature_max = db.Column(db.Float, nullable=False)
    temperature_unit = db.Column(db.String(), default='celsius', nullable=False)
    feels_like_value = db.Column(db.Float, nullable=False)
    feels_like_unit = db.Column(db.String(), default='celsius', nullable=False)
    humidity_value = db.Column(db.Integer, nullable=False)
    humidity_unit = db.Column(db.String(), default='%', nullable=False)
    pressure_value = db.Column(db.Integer, nullable=False)
    pressure_unit = db.Column(db.String(), default='hPa', nullable=False)
    wind_speed_value = db.Column(db.Float, nullable=False)
    wind_speed_unit = db.Column(db.String(), default='m/s', nullable=False)
    wind_speed_name = db.Column(db.String(), nullable=False)
    wind_direction_value_deg = db.Column(db.Integer, nullable=True)
    wind_direction_code = db.Column(db.String(), nullable=True)
    wind_direction_name = db.Column(db.String(), nullable=True)
    cloud_value_pct = db.Column(db.Float, nullable=False)
    cloud_name = db.Column(db.String(), nullable=False)
    visibility_value_m = db.Column(db.Integer, nullable=False)
    precipitation_value_mm = db.Column(db.Float, default=0.0, nullable=False)
    precipitation_mode = db.Column(db.String(), default='no', nullable=False)
    weather_number = db.Column(db.Integer, nullable=False)
    weather_value = db.Column(db.String(), nullable=False)
    weather_icon = db.Column(db.String(), nullable=False)
    lastupdate_value = db.Column(db.DateTime, nullable=True)
