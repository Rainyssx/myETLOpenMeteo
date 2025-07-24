import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import create_engine

url1 = "https://archive-api.open-meteo.com/v1/archive"
url = "https://api.open-meteo.com/v1/forecast"

def getDatafromOpenMeteo(latitude = 55, longitude = 83,start_date = None, end_date = None):

    if start_date  == "" and start_date == "":
        end_date = datetime.now()
        start_date = end_date
        end_date = end_date.strftime("%Y-%m-%d")
        start_date = start_date.strftime("%Y-%m-%d")
    elif start_date  == "":
        start_date = end_date
    elif start_date == "":
        end_date = start_date
    else:
        raise ValueError("Неправильный формат данных даты")


    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,temperature_80m,temperature_120m,wind_speed_10m,wind_speed_80m,wind_direction_10m,wind_direction_80m,visibility,evapotranspiration,weather_code,soil_temperature_0cm,soil_temperature_6cm,rain,showers,snowfall",
        "daily": "sunrise,sunset,daylight_duration",
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "auto",
        "temperature_unit": "celsius",
        "wind_speed_unit": "ms",
        "precipitation_unit": "mm"
    }
    response = requests.get(url, params=params)
    data = response.json()


    # Загрузка в dataframe
    # Данные почасовые
    hourly_data = pd.DataFrame({
        "date": pd.to_datetime([x.split("T")[0] for x in data["hourly"]["time"]], format="%Y-%m-%d"),
        "hour": [int(x.split("T")[1][:2]) for x in data["hourly"]["time"]],
        "relative_humidity_2m": data["hourly"]["relative_humidity_2m"],
        "dew_point_2m": data["hourly"]["dew_point_2m"],
        "visibility": data["hourly"]["visibility"],
        "wind_speed_10m_m_per_s": data["hourly"]["wind_speed_10m"],
        "wind_speed_80m_m_per_s": data["hourly"]["wind_speed_80m"],
        "temperature_2m_celsius": data["hourly"]["temperature_2m"],
        "apparent_temperature_celsius": data["hourly"]["apparent_temperature"],
        "temperature_80m_celsius": data["hourly"]["temperature_80m"],
        "temperature_120m_celsius": data["hourly"]["temperature_120m"],
        "soil_temperature_0cm_celsius": data["hourly"]["soil_temperature_0cm"],
        "soil_temperature_6cm_celsius": data["hourly"]["soil_temperature_6cm"],
        "rain_mm": data["hourly"]["rain"],
        "showers_mm": data["hourly"]["showers"],
        "snowfall_mm": data["hourly"]["snowfall"]
    })

    # Данные daily
    day_data = pd.DataFrame({
        "date": pd.to_datetime(data["daily"]["time"], format="%Y-%m-%d"),
        "sunrise_iso": pd.to_datetime(data["daily"]["sunrise"], format="%Y-%m-%dT%H:%M"),
        "sunset_iso": pd.to_datetime(data["daily"]["sunset"], format="%Y-%m-%dT%H:%M"),
        "daylight_duration": [x / 3600 for x in data["daily"]["daylight_duration"]]
    })

    # merge day and hour data
    fullday_data = hourly_data.merge(day_data, how="inner", on='date')
    # фильтрация по дневным часам
    daylight_data = fullday_data[
        (fullday_data["hour"] >= fullday_data["sunrise_iso"].apply(lambda x: x.hour)) &
        (fullday_data["hour"] <= fullday_data["sunset_iso"].apply(lambda x: x.hour))
        ]

    # Aggregation
    daylight_data = daylight_data.groupby(by="date").agg(
        avg_temperature_2m_daylight=("temperature_2m_celsius", "mean"),
        avg_relative_humidity_2m_daylight=("relative_humidity_2m", "mean"),
        avg_dew_point_2m_daylight=("dew_point_2m", "mean"),
        avg_apparent_temperature_daylight=("apparent_temperature_celsius", "mean"),
        avg_temperature_80m_daylight=("temperature_80m_celsius", "mean"),
        avg_temperature_120m_daylight=("temperature_120m_celsius", "mean"),
        avg_wind_speed_10m_daylight=("wind_speed_10m_m_per_s", "mean"),
        avg_wind_speed_80m_daylight=("wind_speed_80m_m_per_s", "mean"),
        avg_visibility_daylight=("visibility", "mean"),
        total_rain_daylight=("rain_mm", "sum"),
        total_showers_daylight=("showers_mm", "sum"),
        total_snowfall_daylight=("snowfall_mm", "sum"),
    )

    avg_data = fullday_data.groupby(by="date").agg(
        avg_temperature_2m_24h=("temperature_2m_celsius", "mean"),
        avg_relative_humidity_2m_24h=("relative_humidity_2m", "mean"),
        avg_dew_point_2m_24h=("dew_point_2m", "mean"),
        avg_apparent_temperature_24h=("apparent_temperature_celsius", "mean"),
        avg_temperature_80m_24h=("temperature_80m_celsius", "mean"),
        avg_temperature_120m_24h=("temperature_120m_celsius", "mean"),
        avg_wind_speed_10m_24h=("wind_speed_10m_m_per_s", "mean"),
        avg_wind_speed_80m_24h=("wind_speed_80m_m_per_s", "mean"),
        avg_visibility_24h=("visibility", "mean"),
        total_rain_24h=("rain_mm", "sum"),
        total_showers_24h=("showers_mm", "sum"),
        total_snowfall_24h=("snowfall_mm", "sum"),
    )

    # Итоговая таблицы,
    finally_data = fullday_data.drop(columns=[
        "relative_humidity_2m",
        "dew_point_2m",
        "visibility"]
    ).merge(avg_data, on='date').merge(daylight_data, on="date")

    return  finally_data



def outputinFiletoCsv(data, path, nameFile ):
    data.to_csv(path + nameFile)

def outputFiletoDB(data):
    engine = create_engine('postgresql://myuser:mypassword@localhost:5432/db_for_openMeteo')
    data.to_sql('weather_data', engine, if_exists='append', index=False, method='multi')


def is_valid_date_format(date_str):
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return bool(re.fullmatch(pattern, date_str))