from __future__ import annotations

import dataclasses
import datetime as dt


@dataclasses.dataclass
class Forecast:
    feels_like: float
    humidity: float
    id: str | None
    location_id: int
    temp: float
    time: dt.datetime
