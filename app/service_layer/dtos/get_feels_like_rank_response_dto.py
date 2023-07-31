from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class LocationFeelsLike:
    location_name: str
    feels_like: float

    def to_dict(self):
        return dataclasses.asdict(self)


@dataclasses.dataclass
class GetFeelsLikeRankResponseDto:
    items: list[LocationFeelsLike]

    def to_dict(self):
        return dataclasses.asdict(self)
