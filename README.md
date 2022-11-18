# WeatherCacheApp Docker Compose
 Flask server that tracks and stores the weather forecast of specified cities.
  
 Makes use of [Open Weather Map API](https://openweathermap.org/api)
 **(Note: Some functions require paid API key)** \
and Postgres
 
## Current features
- Get and store current forecast
- Get and store forecast data in 3h intervals up to 5 days
- Import historical weather for a city from csv file from [Open Weather Map](https://openweathermap.org/history-bulk)

## Set Environment Variables
create a .env file in the root directory and set the following environment variables
- SECRET_KEY="your secret key"
- DEBUG="1 to enable debug mode"
- FLASK_RUN_HOST=0.0.0.0
- FLASK_RUN_PORT=5000
- SQLALCHEMY_TRACK_MODIFICATIONS=False
- SCHEDULER_API_ENABLED=True
- OPENWEATHERMAP_API_KEY="your key"
- WEATHER_DATA_PATH="path of historical data files"
- POSTGRES_USER="your postgres username"
- POSTGRES_PASSWORD="your postgres pass"
- POSTGRES_DB="your database name" 
- POSTGRES_HOST=db
- POSTGRES_PORT=5432

## Start Server
To rebuild images
```
$ docker compose build -d
```
Run docker
```
$ docker compose up
```

## Check Server Status
See active containers
```
$ docker compose ps
```
Check logs
``` 
$ docker compose logs
```

## Shutdown
``` 
$ docker compose down
```


## Create Database/Tables
Connect to weather app container
``` 
$ docker exec -it  "the container name" /bin/bash
```
Run createdb.py or run the following python code
```
from flaskr import db, create_app
from flaskr.models import *

db.create_all(app=create_app())
```

## Change/Update Database Tables
If you update the table models in models.py run the following python code in the weather app container
```
$ set FLASK_APP=flaskr
$ flask db migrate
$ flask db upgrade
```
## Import Historical Weather Data
- Create an environment variable called WEATHER_DATA_PATH that points to the folder with all the csv data files
**(files must be from Open Weather Maps)**

- or Update ```historical_data_path``` variable in weather.py with desired directory
- Run the app and click Import All and wait
- or chose the specific cities to import

## Helpful Endpoints
- server_address/city_data/get/all - returns the data(not weather) of all the currently tracked cities in an array
formatted:[{city_id,city_name,city_coord_lat,city_coord_long,city_country},...]
- server_address/city_id/get/'latitude,longitude'
returns the city id if the given lat and long match a city that is currently tracked
- ex: .../city_id/get/23,54, -104.45

Requires docker and docker compose installed
