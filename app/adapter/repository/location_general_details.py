from __future__ import annotations

import abc

from app.domain.model import mongo as db
from app.domain.model.location_general_details import LocationGeneralDetails
from infrastructure.mongo_client import get_mongo
from typing import Iterable


class AbstractLocationGeneralDetailsRepository(abc.ABC):
    def get_locations_general_details(self) -> Iterable[LocationGeneralDetails]:
        return self._get_locations_general_details()

    def get_location_general_details_for(self, location_id: str) -> LocationGeneralDetails | None:
        return self._get_location_general_details_for(location_id=location_id)

    @abc.abstractmethod
    def _get_locations_general_details(self) -> Iterable[LocationGeneralDetails]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_location_general_details_for(self, location_id: str) -> LocationGeneralDetails | None:
        raise NotImplementedError


class LocationGeneralDetailsRepository(AbstractLocationGeneralDetailsRepository):
    def _get_locations_general_details(self) -> Iterable[LocationGeneralDetails]:
        collection = get_mongo(db.LocationGeneralDetails)
        response = collection.find()
        for data in response:
            yield LocationGeneralDetails(
                id=str(data.get(db.LocationGeneralDetails.id)),
                location_id=data.get(db.LocationGeneralDetails.location_id),
                name=data.get(db.LocationGeneralDetails.name),
            )

    def _get_location_general_details_for(self, location_id: str) -> LocationGeneralDetails | None:
        collection = get_mongo(db.LocationGeneralDetails)
        response = collection.find_one(
            filter={db.LocationGeneralDetails.location_id: location_id},
        )
        if response:
            return LocationGeneralDetails(
                id=str(response.get(db.LocationGeneralDetails.id)),
                location_id=response.get(db.LocationGeneralDetails.location_id),
                name=response.get(db.LocationGeneralDetails.name),
            )

