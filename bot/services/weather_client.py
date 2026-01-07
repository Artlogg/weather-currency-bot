from __future__ import annotations

from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class WeatherResult:
    city: str
    temperature_c_min: float
    temperature_c_max: float
    wind_speed_ms: float

@dataclass(frozen=True)
class DailyWeatherResult:
    city: str
    date: str
    temperature_c_min: float
    temperature_c_max: float
    wind_speed: float


class WeatherClient:
    def __init__(self, http: httpx.AsyncClient) -> None:
        self._http = http
        
    async def _resolve_city(self, city: str) -> tuple[float, float, str]:
        geo_resp = await self._http.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "ru", "format": "json"},
            timeout=10,
        )
        geo_resp.raise_for_status()

        results = geo_resp.json().get("results") or []
        if not results:
            raise ValueError("CITY_NOT_FOUND")

        place = results[0]
        return (
            place["latitude"],
            place["longitude"],
            place.get("name", city),
        )
    async def get_current_weather(self, city: str) -> WeatherResult:
        lat, lon, resolved_name = await self._resolve_city(city)

        resp = await self._http.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,wind_speed_10m",
                "timezone": "auto",
            },
            timeout=10,
        )
        resp.raise_for_status()

        current = resp.json()["current"]

        return WeatherResult(
            city=resolved_name,
            temperature_c=float(current["temperature_2m"]),
            wind_speed_ms=float(current["wind_speed_10m"]),
        )
    async def get_week_forecast(self, city: str) -> list[DailyWeatherResult]:
        lat, lon, resolved_name = await self._resolve_city(city)

        resp = await self._http.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": (
                    "temperature_2m_min,"
                    "temperature_2m_max,"
                    "wind_speed_10m_max"
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
                temperature_c_min=float(daily["temperature_2m_min"][i]),
                temperature_c_max=float(daily["temperature_2m_max"][i]),
                wind_speed=float(daily["wind_speed_10m_max"][i]),
            )
            for i in range(len(daily["time"]))
        ]
