from __future__ import annotations

import dataclasses

@dataclasses.dataclass
class DayAverageTemperature:
    location: str
    temp: float
    date: str


@dataclasses.dataclass
class DailyAverageTemperatureResponseDto:
    items: list[DayAverageTemperature]

    def to_dict(self) -> dict[str, list[dict[str, float]]]:
        response = {}
        for item in self.items:
            if item.location not in response:
                response[item.location] = []
            response[item.location].append({item.date: item.temp})
        return response
