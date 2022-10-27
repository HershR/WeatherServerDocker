# WeatherCacheApp
 Flask server that tracks and stores the weather forecast of specified cities.
  
 Makes use of [Open Weather Map API](https://openweathermap.org/api)
 **(Note: Some functions require paid API key)**
 
## Current features
- Get and store current forecast
- Get and store forecast data in 3h intervals up to 5 days
- Import historical weather for a city from csv file from [Open Weather Map](https://openweathermap.org/history-bulk)


## Set Open Weather Maps API Key
- Create an environment variable called OPENWEATHERMAP_API_KEY and set it to your key
```
$ set OPENWEATHERMAP_API_KEY="key"
```
or
- Replace owm_api_key variable in weather.py and cities.py with desired key

## Set Database URL
- Create an environment variable called DATABASE_URL and set it to your database url/location
- ex postgres:
```
$ set DATABASE_URL=postgres://"username":"password""host"/"databasename"
```
- Note: the database models in models.py make use of Datatime types

## Create Database/Tables
Run the following script in python 
```
from flaskr import db, create_app
from flaskr.models import *

db.create_all(app=create_app())
```
## Run Locally
```
$ set FLASK_APP=flaskr
$ set FLASK_ENV=development
$ set FLASK_DEBUG=1
$ flask run
```
## Change/Update Database Tables
If you update the table models in models.py
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


Required Packages in requirements.txt
