# List of all API calls

## Get City ID by Coordinates
Get the city ID for a specific city using latitude and longitude coordinates

API call http://<weatherserver_address>/get_location_id?lat={latitude}&long={longitude}

Example call
```
http://<weatherserver_address>/get_location_id?lat=42.6526&long=-73.7562
```
Example output
```
5106834
```


## Get all City IDs
Get the city ID for every tracked city in json format

API call http://<weatherserver_address>/get_location_ids

Example output
```json
{
  "Albany": "5106834",
  "Moline": "4902476"
}
```

## Get all City Data
Get the City information for all cities in json format

API call http://<weatherserver_address>/get_location_data

Example output
```json
{
  "Albany": {"city_id": "5106834", "city_name": "Albany", "city_coord_lat": "42.6526", "city_coord_long": "-73.7562", "city_country": "US"},
  "Moline": {"city_id": "4902476", "city_name": "Moline", "city_coord_lat": "41.5081", "city_coord_long": "-90.5163", "city_country": "US"}}
```

## Get City Weather By Date
Get the weather data for a specific city at a specific time in json format

API call  **http://<weatherserver_address>/get_weather_by_date?id={location id}&date={date}**

Parameters
- location id: [Get City ID](#Get City ID by Coordinates)
- date: provide date in iso-8601 utc timestamp - YYYY-MM-DDTHH:MM:SS

Example call
```
http://<weatherserver_address>/get_weather_by_date?id=5106834&date=2022-12-10T18:00:00
```
Example Output
```json
{
  "type": "forecast", 
  "is_found": false, 
  "request_timestamp": "2022-12-08 23:21:00",
  "forecast_timestamp": "2022-12-10 18:00:00",
  "city_id": "5106834",
  "city_sun_rise": "2022-12-08 12:12:37",
  "city_sun_set": "2022-12-08 21:21:34",
  "timezone_offset": "-18000",
  "temperature_value": "0.79",
  "temperature_min": "0.79",
  "temperature_max": "0.79",
  "temperature_unit": "celsius",
  "feels_like_value": "-1.15",
  "feels_like_unit": "celsius",
  "humidity_value": "56",
  "humidity_unit": "%",
  "pressure_value": "1031",
  "pressure_unit": "hPa",
  "wind_speed_value": "1.7",
  "wind_speed_unit": "m/s",
  "wind_speed_name": "Light breeze",
  "wind_direction_value_deg": "357",
  "wind_direction_code": "N",
  "wind_direction_name": "North",
  "cloud_value_pct": "0.0",
  "cloud_name": "clear sky",
  "visibility_value_m": "10000",
  "precipitation_value_mm": "0.0",
  "precipitation_mode": "no",
  "weather_number": "800",
  "weather_value": "clear sky",
  "weather_icon": "01d",
  "lastupdate_value": "None"
}
```
Fields in Response
- type: current or forecast
- is_found: True is data for the given time was found in the hourly updated database.
- rest refer to [current](https://openweathermap.org/current) or [forecast](https://openweathermap.org/forecast5)
