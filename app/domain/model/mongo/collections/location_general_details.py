from app.domain.model.mongo.abstract_collection import AbstractCollection


class LocationGeneralDetails(AbstractCollection):
    __collection_name__ = 'location_general_details'

    location_id = 'location_id'
    name = 'name'
