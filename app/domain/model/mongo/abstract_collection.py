from __future__ import annotations

import abc


class AbstractCollection(abc.ABC):
    __collection_name__: str | None = None
    __indexes__: list[dict] | None = None

    id: str = '_id'

    def get_collection_name(self) -> str:
        return self.__collection_name__
