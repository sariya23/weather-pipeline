from dataclasses import dataclass
from datetime import date
from typing import Self


@dataclass
class GetWeatherRequestDTO:
    latitude: float
    longitude: float
    hourly: list[str] | None = None
    start_date: date | None = None
    end_date: date | None = None

    @classmethod
    def moscow(
        cls,
        hourly: list[str] | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> Self:
        return cls(
            latitude=55.75,
            longitude=37.62,
            hourly=hourly,
            start_date=start_date,
            end_date=end_date,
        )
