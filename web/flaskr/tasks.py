from .weather import city_ids, update_current_weather, update_forcast_3h
from .extensions import scheduler


# task intervals
# in seconds
update_current_interval = 60  #3600  # one hour
update_forecast_interval = 120  #86400  # one day


#updated the current weather for all cities
@scheduler.task('interval', id='update_current_weather_all', seconds=update_current_interval, misfire_grace_time=900)
def update_current_weather_all():
    print("update current all")
    with scheduler.app.app_context():
        for id in city_ids():
            update_current_weather(id)

#update the current forecast for all cities
@scheduler.task('interval', id='update_current_forecast_all', seconds=update_forecast_interval, misfire_grace_time=900)
def update_current_forecast_all():
    print("update forecast all")
    with scheduler.app.app_context():
        for id in city_ids():
            update_forcast_3h(id)
