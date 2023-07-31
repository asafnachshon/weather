from __future__ import annotations

import abc
from typing import Iterable

from app.adapter.repository.forecast import AbstractForcastRepository, ForcastRepository, DailyAverageMeasurements
from app.adapter.repository.location_general_details import (
    AbstractLocationGeneralDetailsRepository,
    LocationGeneralDetailsRepository,
)
from app.domain.model.forecast import Forecast
from app.domain.model.location_general_details import LocationGeneralDetails
from app.service_layer.dtos.get_daily_average_temperature_response_dto import (
    DailyAverageTemperatureResponseDto,
    DayAverageTemperature,
)
from app.service_layer.dtos.get_feels_like_rank_request_dto import GetFeelsLikeRankRequestDto
from app.service_layer.dtos.get_feels_like_rank_response_dto import GetFeelsLikeRankResponseDto, LocationFeelsLike
from app.service_layer.dtos.get_lowest_humidity_point_response_dto import GetLowestHumidityPointResponseDto


class AbstractForcastService(abc.ABC):
    def __init__(
            self,
            forecast_repository: AbstractForcastRepository,
            location_general_details_repository: AbstractLocationGeneralDetailsRepository,
    ):
        self._forcast_repository = forecast_repository
        self._location_repository = location_general_details_repository

    def _get_locations_name_by_location_id(self) -> dict[int, str]:
        locations: Iterable[LocationGeneralDetails] = self._location_repository.get_locations_general_details()
        return {location.location_id: location.name for location in locations}

    def get_daily_average_temperature(self) -> DailyAverageTemperatureResponseDto:
        location_name_by_id: dict[int, str] = self._get_locations_name_by_location_id()
        day_averages: Iterable[DailyAverageMeasurements] = self._forcast_repository.get_day_average_measurements_for(
            location_ids=list(location_name_by_id.keys()),
        )
        return DailyAverageTemperatureResponseDto(
            items=[
                    DayAverageTemperature(
                        location=location_name_by_id[item.location_id],
                        temp=item.temp,
                        date=item.time,
                    )
                    for item in day_averages
            ],
        )

    def get_lowest_humid_point(self):
        minimum_humidity_point: Forecast | None = self._forcast_repository.get_minimum_humidity_point()
        if not minimum_humidity_point:
            raise Exception('No minimum humidity point')

        location: LocationGeneralDetails | None = self._location_repository.get_location_general_details_for(
            location_id=minimum_humidity_point.location_id,
        )
        if not location:
            raise Exception('No humidity point location')

        return GetLowestHumidityPointResponseDto(
            humidity=minimum_humidity_point.humidity,
            location=location.name,
            time=minimum_humidity_point.time,
        )

    def get_feels_like_rank(self, request: GetFeelsLikeRankRequestDto) -> GetFeelsLikeRankResponseDto:
        location_name_by_id: dict[int, str] = self._get_locations_name_by_location_id()
        farthest_measurements: list[Forecast] = self._forcast_repository.get_farthest_measurements(
            location_ids=list(location_name_by_id.keys()),
        )
        items = [
            LocationFeelsLike(
                location_name=location_name_by_id.get(item.location_id),
                feels_like=item.feels_like,
            )
            for item in farthest_measurements
        ]

        return GetFeelsLikeRankResponseDto(
            items=sorted(items, key=lambda item: item.feels_like, reverse=request.desc)
        )


class ForcastService(AbstractForcastService):
    def __init__(self):
        super().__init__(
            forecast_repository=ForcastRepository(),
            location_general_details_repository=LocationGeneralDetailsRepository()
        )
