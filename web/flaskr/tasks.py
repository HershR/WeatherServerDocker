from .weather import city_ids, update_current_weather, update_forcast_3h
from .extensions import scheduler



#updated the current weather for all cities
@scheduler.task('cron', id='update_current_weather_all', minute=0, misfire_grace_time=900)
def update_current_weather_all():
    print("update current all")
    with scheduler.app.app_context():
        for id in city_ids():
            update_current_weather(id)

#update the current forecast for all cities
@scheduler.task('cron', id='update_current_forecast_all', hour=0, misfire_grace_time=900)
def update_current_forecast_all():
    print("update forecast all")
    with scheduler.app.app_context():
        for id in city_ids():
            update_forcast_3h(id)
