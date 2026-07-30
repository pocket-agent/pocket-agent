"""Current weather via Open-Meteo (no API key)."""

from __future__ import annotations

import logging
from datetime import datetime
from zoneinfo import ZoneInfo

import httpx

from pocket_agent.tools.base import ToolResult

logger = logging.getLogger(__name__)

_WMO_WEATHER: dict[int, str] = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Heavy rain showers",
    95: "Thunderstorm",
}


def _weather_label(code: int | None) -> str:
    if code is None:
        return "unknown"
    return _WMO_WEATHER.get(int(code), f"code {code}")


async def current_weather(location: str) -> ToolResult:
    place = (location or "").strip()
    if not place:
        return ToolResult(success=False, error="location is required")

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            geo = await client.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": place, "count": 1, "language": "en", "format": "json"},
            )
            geo.raise_for_status()
            geo_data = geo.json()
            results = geo_data.get("results") or []
            if not results:
                return ToolResult(success=False, error=f"No location found for '{place}'")

            hit = results[0]
            lat = hit["latitude"]
            lon = hit["longitude"]
            name = hit.get("name", place)
            country = hit.get("country", "")
            tz_name = hit.get("timezone", "UTC")

            forecast = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
                    "timezone": tz_name,
                },
            )
            forecast.raise_for_status()
            fc = forecast.json()
            current = fc.get("current") or {}

            local_time = datetime.now(ZoneInfo(tz_name)).strftime("%Y-%m-%d %H:%M %Z")
            temp = current.get("temperature_2m")
            humidity = current.get("relative_humidity_2m")
            wind = current.get("wind_speed_10m")
            code = current.get("weather_code")

            summary = (
                f"{name}, {country}: {temp}°C, {_weather_label(code)}, "
                f"humidity {humidity}%, wind {wind} km/h. Local time: {local_time}."
            )

            return ToolResult(
                success=True,
                data={
                    "location": name,
                    "country": country,
                    "latitude": lat,
                    "longitude": lon,
                    "timezone": tz_name,
                    "local_time": local_time,
                    "temperature_c": temp,
                    "humidity_percent": humidity,
                    "wind_speed_kmh": wind,
                    "conditions": _weather_label(code),
                    "summary": summary,
                },
            )
    except httpx.HTTPError as exc:
        logger.exception("current_weather HTTP error")
        return ToolResult(success=False, error=f"Weather service error: {exc}")
    except Exception as exc:
        logger.exception("current_weather failed")
        return ToolResult(success=False, error=str(exc))
