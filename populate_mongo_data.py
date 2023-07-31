from __future__ import annotations

import dataclasses
import datetime as dt
import requests

from app.domain.model import mongo as db
from app.domain.model.location_general_details import LocationGeneralDetails
from bson import json_util
from infrastructure.consts import CITIES, DATETIME_FORMAT, OPEN_WEATHER_HOST
from infrastructure.mongo_client import get_mongo
from requests import Response

API_KEY = '41573e0321bd6310e36679d8f3389a80'


@dataclasses.dataclass
class CityGeocoding:
    lat: float
    lon: float
    name: str


@dataclasses.dataclass
class Forecast:
    date: dt.datetime
    humidity: float
    feels_like: float
    temp: float

    @classmethod
    def from_dict(cls, data: dict) -> Forecast:
        main = data.get('main', {})
        return cls(
            date=dt.datetime.strptime(data['dt_txt'], DATETIME_FORMAT),
            humidity=main.get('humidity'),
            feels_like=main.get('feels_like'),
            temp=main.get('temp'),
        )


@dataclasses.dataclass
class FiveDaysCityForecast:
    city: LocationGeneralDetails
    forecasts: list[Forecast]

    @classmethod
    def from_dict(cls, data: dict) -> FiveDaysCityForecast:
        location_general_details = LocationGeneralDetails(
            location_id=data.get('city', {}).get('id'),
            name=data.get('city', {}).get('name'),
        )
        return cls(
            city=location_general_details,
            forecasts=[Forecast.from_dict(data=forecast) for forecast in data.get('list', {})],
        )


def _get_request(path: str, params: dict):
    params['appid'] = API_KEY
    response: Response = requests.get(url=f'{OPEN_WEATHER_HOST}/{path}', params=params)
    return json_util.loads(response.content)


def _get_geocoding_for(city: str) -> CityGeocoding:
    content: list[dict] = _get_request(
        path='geo/1.0/direct',
        params=dict(q=city),
    )
    data: dict = content[0]
    return CityGeocoding(lat=data['lat'], lon=data['lon'], name=data['name'])


def _get_five_days_three_hour_forecast(latitude: float, longitude: float) -> FiveDaysCityForecast:
    content = _get_request(
        path='data/2.5/forecast',
        params=dict(
            lat=latitude,
            lon=longitude,
            units='metric'
        ),
    )
    return FiveDaysCityForecast.from_dict(data=content)


def _get_city_five_days_three_hour_forecast(city: str) -> FiveDaysCityForecast:
    geocoding: CityGeocoding = _get_geocoding_for(city=city)
    return _get_five_days_three_hour_forecast(latitude=geocoding.lat, longitude=geocoding.lon)


def _save_to_location_general_details_collection(request: LocationGeneralDetails) -> None:
    collection = get_mongo(collection=db.LocationGeneralDetails)
    collection.insert_one(
        document={
            db.LocationGeneralDetails.location_id: request.location_id,
            db.LocationGeneralDetails.name: request.name,
        },
    )


def _save_city_forecasts_for(request: FiveDaysCityForecast):
    collection = get_mongo(collection=db.Forecasts)
    collection.insert_many(
        documents=[
            {
                db.Forecasts.feels_like: forecast.feels_like,
                db.Forecasts.humidity: forecast.humidity,
                db.Forecasts.location_id: request.city.location_id,
                db.Forecasts.temp: forecast.temp,
                db.Forecasts.time: forecast.date,
            }
            for forecast in request.forecasts
        ],
    )


def save_city_forecasts_data_to_mongodb(city: str) -> None:
    city_forecasts: FiveDaysCityForecast = _get_city_five_days_three_hour_forecast(city=city)
    _save_to_location_general_details_collection(request=city_forecasts.city)
    _save_city_forecasts_for(request=city_forecasts)


def drop_collections():
    get_mongo(collection=db.LocationGeneralDetails).drop()
    get_mongo(collection=db.Forecasts).drop()


def create_collections_indexes():
    for db_collection in [db.Forecasts, db.LocationGeneralDetails]:
        if db_collection.__indexes__:
            collection = get_mongo(collection=db_collection)
            for index in db_collection.__indexes__:
                collection.create_index(**index)


if __name__ == '__main__':
    drop_collections()
    create_collections_indexes()
    for city_name in CITIES:
        save_city_forecasts_data_to_mongodb(city=city_name)
