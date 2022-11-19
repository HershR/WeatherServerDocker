import os
from pytz import utc
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
#DEBUG = True
#FLASK_RUN_HOST = '0.0.0.0'
#FLASK_RUN_PORT = 5000

SCHEDULER_API_ENABLED = True
SCHEDULER_TIMEZONE = utc

OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
WEATHER_DATA_PATH = "HistoricalWeatherData"

pg_user = os.getenv("POSTGRES_USER")
pg_pass = os.getenv("POSTGRES_PASSWORD")
pg_db = os.getenv("POSTGRES_DB")
pg_host = os.getenv("POSTGRES_HOST")
pg_port = os.getenv("POSTGRES_PORT")

SQLALCHEMY_DATABASE_URI = \
    f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
