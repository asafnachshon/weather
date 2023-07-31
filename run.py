from __future__ import annotations

from app.domain.schema.feels_like_rank import FEELS_LIKE_RANK_SCHEMA
from app.service_layer.dtos.get_feels_like_rank_request_dto import GetFeelsLikeRankRequestDto
from app.service_layer.dtos.get_feels_like_rank_response_dto import GetFeelsLikeRankResponseDto
from app.service_layer.dtos.get_lowest_humidity_point_response_dto import GetLowestHumidityPointResponseDto
from app.service_layer.forecast_service import ForcastService, DailyAverageTemperatureResponseDto
from flask import Flask, request

app = Flask(__name__)


@app.get('/avg_tmp_per_city_per_day')
def avg_tmp_per_city_per_day() -> dict:
    service = ForcastService()
    response: DailyAverageTemperatureResponseDto = service.get_daily_average_temperature()
    return response.to_dict()


@app.get('/lowest_humid')
def lowest_humid() -> dict:
    service = ForcastService()
    response: GetLowestHumidityPointResponseDto = service.get_lowest_humid_point()
    return response.to_dict()


@app.route('/feels_like_rank', methods=['GET'])
def feels_like_rank() -> dict:
    params: dict = FEELS_LIKE_RANK_SCHEMA(dict(request.args))
    service = ForcastService()
    response: GetFeelsLikeRankResponseDto = service.get_feels_like_rank(
        request=GetFeelsLikeRankRequestDto(
            desc=params.get('order_dir', 'desc') == 'desc',
        ),
    )
    return response.to_dict()
