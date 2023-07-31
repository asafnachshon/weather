from app.domain.model.mongo.abstract_collection import AbstractCollection


class LocationGeneralDetails(AbstractCollection):
    __collection_name__ = 'location_general_details'

    location_id = 'location_id'
    name = 'name'

    __indexes__ = [
        dict(
            keys=[(location_id, 1)],
            name='location_id_1'
        ),
    ]
