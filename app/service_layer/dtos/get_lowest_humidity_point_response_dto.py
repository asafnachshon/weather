from __future__ import annotations

import dataclasses
import datetime as dt

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


@dataclasses.dataclass
class GetLowestHumidityPointResponseDto:
    humidity: float
    location: str
    time: dt.datetime

    def to_dict(self):
        return dict(
            humidity=self.humidity,
            location=self.location,
            time=self.time.strftime(DATETIME_FORMAT)
        )
