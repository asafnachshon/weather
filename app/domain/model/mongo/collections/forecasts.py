from app.domain.model.mongo.abstract_collection import AbstractCollection


class Forecasts(AbstractCollection):
    __collection_name__ = 'forecasts'

    feels_like = 'feels_like'
    humidity = 'humidity'
    location_id = 'location_id'
    temp = 'temp'
    time = 'time'

    __indexes__ = [
        dict(
            keys=[(humidity, 1)],
            name='humidity_1',
        ),
        dict(
            keys=[(location_id, 1), (time, -1)],
            name='location_id_1_time_desc',
        ),
    ]
