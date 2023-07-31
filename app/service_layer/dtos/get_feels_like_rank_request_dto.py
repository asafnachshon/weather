from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class GetFeelsLikeRankRequestDto:
    desc: bool | None
