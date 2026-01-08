from __future__ import annotations

from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class DailyWeatherResult:
    city: str
    date: str  # YYYY-MM-DD
    temperature_min: float
    temperature_max: float
    wind_speed_max: float


class WeatherClient:
    def __init__(self, http: httpx.AsyncClient) -> None:
        self.http = http

    async def _resolve_city(self, city: str) -> tuple[float, float, str]:
        resp = await self.http.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "ru", "format": "json"},
            timeout=10,
        )
        resp.raise_for_status()

        results = resp.json().get("results") or []
        if not results:
            raise ValueError("CITY_NOT_FOUND")

        place = results[0]
        return place["latitude"], place["longitude"], place.get("name", city)

    async def get_week_forecast(self, city: str) -> list[DailyWeatherResult]:
        lat, lon, resolved_name = await self._resolve_city(city)

        resp = await self.http.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": (
                    "temperature_2m_min,"
                    "temperature_2m_max,"
                    "wind_speed_10m_max,"
                    "weathercode"
                ),
                "forecast_days": 7,
                "timezone": "auto",
            },
            timeout=10,
        )
        resp.raise_for_status()

        daily = resp.json()["daily"]

        return [
            DailyWeatherResult(
                city=resolved_name,
                date=daily["time"][i],
                temperature_min=daily["temperature_2m_min"][i],
                temperature_max=daily["temperature_2m_max"][i],
                weather_codes=daily["weathercode"][i],
                wind_speed_max=daily["wind_speed_10m_max"][i],
            )
            for i in range(len(daily["time"]))
        ]
