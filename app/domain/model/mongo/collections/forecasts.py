from app.domain.model.mongo.abstract_collection import AbstractCollection


class Forecasts(AbstractCollection):
    __collection_name__ = 'forecasts'

    feels_like = 'feels_like'
    humidity = 'humidity'
    location_id = 'location_id'
    temp = 'temp'
    time = 'time'
