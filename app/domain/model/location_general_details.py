from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class LocationGeneralDetails:
    location_id: int
    name: str
    id: str | None = None
