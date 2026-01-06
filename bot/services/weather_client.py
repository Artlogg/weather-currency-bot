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
    wind_speed_max: float


class WeatherClient:
    def __init__(self, http: httpx.AsyncClient) -> None:
        self._http = http

    async def get_current_weather(self, city: str) -> WeatherResult:
        geo_resp = await self._http.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1,
                    "language": "ru", "format": "json"},
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
                "current": ("temperature_2m_min,"
                            "temperature_2m_max,"
                            "wind_speed_10m,"
                ),
                "timezone": "auto",
            },
            timeout=10,
        )
        w_resp.raise_for_status()
        w_data = w_resp.json()
        current = w_data.get("current") or {}

        return WeatherResult(
            city=resolved_name,
            temperature_c_min=float(current["temperature_2m_min"]),
            temperature_c_max=float(current["temperature_2m_max"]),
            wind_speed_ms=float(current["wind_speed_10m"]),
        )
    async def get_week_forecast(self, city: str) -> list[DailyWeatherResult]:
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
        # 2) Weekly forecast
        w_resp = await self._http.get(
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
        w_resp.raise_for_status()
        w_data = w_resp.json()
        daily = w_data.get("daily") or {}

        dates = daily.get("time", [])
        temp_min = daily.get("temperature_2m_min", [])
        temp_max = daily.get("temperature_2m_max", [])
        wind_max = daily.get("wind_speed_10m_max", [])

        forecast: list[DailyWeatherResult] = []

        for i in range(len(dates)):
            forecast.append(
                DailyWeatherResult(
                    city=resolved_name,
                    date=dates[i],
                    temperature_min=float(temp_min[i]),
                    temperature_max=float(temp_max[i]),
                    wind_speed_max=float(wind_max[i]),
                )
            )

        return forecast
