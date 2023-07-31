from __future__ import annotations

import abc
import dataclasses

from app.domain.model import mongo as db
from app.domain.model.forecast import Forecast
from infrastructure.mongo_client import get_mongo
from typing import Iterable

DATE_FORMAT = '%Y-%m-%d'


@dataclasses.dataclass
class DailyAverageMeasurements:
    location_id: int
    temp: float
    time: str


class AbstractForcastRepository(abc.ABC):
    def get_day_average_measurements_for(self, location_ids: list[int]) -> Iterable[DailyAverageMeasurements]:
        return self._get_day_average_measurements_for(location_ids=location_ids)

    def get_minimum_humidity_point(self) -> Forecast | None:
        return self._get_minimum_humidity_point()

    def get_farthest_measurements(self, location_ids: list[int]) -> list[Forecast]:
        return self._get_farthest_measurements(location_ids=location_ids)

    @abc.abstractmethod
    def _get_day_average_measurements_for(self, location_ids: list[int]) -> Iterable[DailyAverageMeasurements]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_minimum_humidity_point(self) -> Forecast | None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_farthest_measurements(self, location_ids: list[int]) -> list[Forecast]:
        raise NotImplementedError


class ForcastRepository(AbstractForcastRepository):
    def _get_day_average_measurements_for(self, location_ids: list[int]) -> Iterable[DailyAverageMeasurements]:
        collection = get_mongo(db.Forecasts)
        response = collection.aggregate([
            {
                '$match': {
                    db.Forecasts.location_id: {'$in': location_ids}
                }
            },
            {
                '$project': {
                    db.Forecasts.time: {
                        '$dateToString': {
                            'format': DATE_FORMAT,
                            'date': f'${db.Forecasts.time}',
                        },
                    },
                    db.Forecasts.location_id: 1,
                    db.Forecasts.temp: 1,
                },
            },
            {
                '$group': {
                    '_id': {
                        db.Forecasts.location_id: f'${db.Forecasts.location_id}',
                        db.Forecasts.time: f'${db.Forecasts.time}',
                    },
                    db.Forecasts.temp: {'$avg': f'${db.Forecasts.temp}'},
                },
            }
        ])
        for data in response:
            yield DailyAverageMeasurements(
                location_id=data[db.Forecasts.id].get(db.Forecasts.location_id),
                temp=data.get(db.Forecasts.temp),
                time=data[db.Forecasts.id].get(db.Forecasts.time),
            )

    def _get_minimum_humidity_point(self) -> Forecast | None:
        collection = get_mongo(db.Forecasts)
        response: list[dict] = list(collection.find().sort([(db.Forecasts.humidity, 1)]).limit(1))
        if response:
            data: dict = response[0]
            return Forecast(
                feels_like=data.get(db.Forecasts.feels_like),
                humidity=data.get(db.Forecasts.humidity),
                id=str(data[db.Forecasts.id]),
                location_id=data.get(db.Forecasts.location_id),
                temp=data.get(db.Forecasts.temp),
                time=data.get(db.Forecasts.time),
            )

    def _get_farthest_measurements(self, location_ids: list[int]) -> list[Forecast]:
        collection = get_mongo(db.Forecasts)
        response = collection.aggregate([
            {
                '$match': {
                    db.Forecasts.location_id: {'$in': location_ids},
                },
            },
            {
                '$sort': {db.Forecasts.time: -1},
            },
            {
                '$group': {
                    '_id': f'${db.Forecasts.location_id}',
                    db.Forecasts.feels_like: {'$first': f'${db.Forecasts.feels_like}'},
                    db.Forecasts.humidity: {'$first': f'${db.Forecasts.humidity}'},
                    db.Forecasts.temp: {'$first': f'${db.Forecasts.temp}'},
                    db.Forecasts.time: {'$first': f'${db.Forecasts.time}'},
                },
            },
        ])
        return [
            Forecast(
                feels_like=data.get(db.Forecasts.feels_like),
                humidity=data.get(db.Forecasts.humidity),
                id=None,
                location_id=data.get(db.Forecasts.id),
                temp=data.get(db.Forecasts.temp),
                time=data.get(db.Forecasts.time),
            )
            for data in response
        ]
