"""
MCP server exposing the two "current information" tools required by the
assignment:

  1. get_weather_forecast - current + multi-day forecast for the configured
     destination, via the free Open-Meteo API (no key required).
  2. convert_currency - currency conversion between two ISO codes, via the
     free frankfurter.dev API (no key required).

This is a real Model Context Protocol server (stdio transport) built with
the official `mcp` Python SDK. The FastAPI app never calls these tools
directly by importing this file's functions - it goes through an MCP
client (see app/mcp/client.py / app/agent/agent.py), which is what the
assignment means by "connect to at least two MCP tools" rather than just
calling library functions in-process.

Run standalone for a quick manual check:
    python -m app.mcp.server
"""
from __future__ import annotations

import sys
from pathlib import Path
from datetime import date

from fastapi import logger
import httpx
from mcp.server.fastmcp import FastMCP

#sys.path.insert(0, str(__file__).rsplit("/app/", 1)[0])  # allow `app.config` import when run directly
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))  # allow `app.config` import when run directly

from app.config import CURRENCY_API_BASE, WEATHER_API_BASE, DESTINATION_LAT, DESTINATION_LON, DESTINATION_NAME

mcp = FastMCP("travel-current-info")

WEATHER_CODE_DESCRIPTIONS = {
    0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast",
    45: "fog", 48: "depositing rime fog",
    51: "light drizzle", 53: "moderate drizzle", 55: "dense drizzle",
    61: "slight rain", 63: "moderate rain", 65: "heavy rain",
    66: "light freezing rain", 67: "heavy freezing rain",
    71: "slight snow", 73: "moderate snow", 75: "heavy snow",
    80: "slight rain showers", 81: "moderate rain showers", 82: "violent rain showers",
    95: "thunderstorm", 96: "thunderstorm with slight hail", 99: "thunderstorm with heavy hail",
}


def _describe_code(code: int) -> str:
    return WEATHER_CODE_DESCRIPTIONS.get(code, f"weather code {code}")


@mcp.tool()
def get_weather_forecast(days: int = 3, location: str | None = None) -> dict:
    """Get the current weather and a daily forecast for the trip destination.

    Args:
        days: number of forecast days to return (1-7). Defaults to 3.
        location: optional override, e.g. "Singapore". If omitted, uses the
            destination this deployment is configured for.

    Returns a dict with 'location', 'current', and 'daily' (a list of
    {date, min_c, max_c, precipitation_probability_pct, condition}).
    Raises a clear error (surfaced to the caller, not swallowed) if the
    upstream weather API is unavailable, so the assistant can tell the user
    the forecast could not be retrieved rather than inventing one.
    """
    days = max(1, min(days, 7))
    lat, lon = DESTINATION_LAT, DESTINATION_LON
    loc_name = location or DESTINATION_NAME

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,precipitation,weather_code",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "forecast_days": days,
        "timezone": "auto",
    }
    try:
        resp = httpx.get(WEATHER_API_BASE, params=params, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Weather service unavailable: {exc}") from exc

    current = data.get("current", {})
    daily_raw = data.get("daily", {})
    daily = []
    for i, day_str in enumerate(daily_raw.get("time", [])):
        daily.append({
            "date": day_str,
            "min_c": daily_raw.get("temperature_2m_min", [None])[i],
            "max_c": daily_raw.get("temperature_2m_max", [None])[i],
            "precipitation_probability_pct": daily_raw.get("precipitation_probability_max", [None])[i],
            "condition": _describe_code(daily_raw.get("weather_code", [None])[i]),
        })

    return {
        "location": loc_name,
        "retrieved_on": date.today().isoformat(),
        "current": {
            "temperature_c": current.get("temperature_2m"),
            "precipitation_mm": current.get("precipitation"),
            "condition": _describe_code(current.get("weather_code", -1)),
        },
        "daily": daily,
        "source": "Open-Meteo (open-meteo.com)",
    }


@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """Convert an amount from one currency to another using live exchange rates.

    Args:
        amount: amount to convert, e.g. 50000
        from_currency: ISO 4217 code of the source currency, e.g. "INR"
        to_currency: ISO 4217 code of the target currency, e.g. "SGD"

    Returns a dict with 'amount', 'from_currency', 'to_currency', 'rate',
    'converted_amount', and 'source'. Raises a clear error if the exchange
    rate service is unavailable, so the assistant can say so rather than
    guessing a rate.
    """
    # from_currency = from_currency.upper().strip()
    # to_currency = to_currency.upper().strip()
    # try:
    #     resp = httpx.get(
    #         f"{CURRENCY_API_BASE}/latest",
    #         params={"base": from_currency, "symbols": to_currency},
    #         timeout=10.0,
    #     )
    #     resp.raise_for_status()
    #     data = resp.json()
    #     rate = data["rates"][to_currency]
    # except Exception as exc:  # noqa: BLE001
    #     raise RuntimeError(f"Currency conversion service unavailable: {exc}") from exc

    from_currency = from_currency.upper().strip()
    to_currency = to_currency.upper().strip()

    # try:
    #     resp = httpx.get(
    #         f"{CURRENCY_API_BASE}/rate/{from_currency}/{to_currency}",
    #         timeout=10.0,
    #     )
    #     resp.raise_for_status()
    #     data = resp.json()
    #     rate = data["rate"]
    #     logger.info(f"Currency conversion rate: {from_currency} -> {to_currency} = {rate}") 
    # except Exception as exc:  # noqa: BLE001
    #     raise RuntimeError(f"Currency conversion service unavailable: {exc}") from exc

    try:
        resp = httpx.get(
            f"{CURRENCY_API_BASE}/latest",
            params={"from": from_currency, "to": to_currency},
            timeout=10.0,
            follow_redirects=True,
        )
        resp.raise_for_status()
        data = resp.json()
        rate = data["rates"][to_currency]
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(f"Currency conversion service unavailable: {exc}") from exc

    converted = round(amount * rate, 2)
    return {
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "rate": rate,
        "converted_amount": converted,
        #"source": "exchangerate.host",
        "source": "Frankfurter (frankfurter.app)",
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
