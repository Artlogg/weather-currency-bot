from __future__ import annotations

from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class WeatherResult:
    city: str
    temperature_c: float
    wind_speed_ms: float


class WeatherClient:
    def __init__(self, http: httpx.AsyncClient) -> None:
        self._http = http

    async def get_current_weather(self, city: str) -> WeatherResult:
        # 1) Geocoding: city -> lat/lon
        geo_resp = await self._http.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "ru", "format": "json"},
            timeout=10,
        )
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()
        results = geo_data.get("results") or []
        if not results:
            raise ValueError("CITY_NOT_FOUND")

        place = results[0]
        lat = place["latitude"]
        lon = place["longitude"]
        resolved_name = place.get("name", city)

        # 2) Current weather by lat/lon
        w_resp = await self._http.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,wind_speed_10m",
                "timezone": "auto",
            },
            timeout=10,
        )
        w_resp.raise_for_status()
        w_data = w_resp.json()
        current = w_data.get("current") or {}

        return WeatherResult(
            city=resolved_name,
            temperature_c=float(current["temperature_2m"]),
            wind_speed_ms=float(current["wind_speed_10m"]),
        )
