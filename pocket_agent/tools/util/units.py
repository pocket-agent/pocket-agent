"""Unit conversion for common quantities."""

from __future__ import annotations

from pocket_agent.tools.base import ToolResult

_LENGTH_TO_M = {
    "m": 1.0,
    "meter": 1.0,
    "meters": 1.0,
    "km": 1000.0,
    "kilometer": 1000.0,
    "kilometers": 1000.0,
    "mi": 1609.344,
    "mile": 1609.344,
    "miles": 1609.344,
    "ft": 0.3048,
    "foot": 0.3048,
    "feet": 0.3048,
    "in": 0.0254,
    "inch": 0.0254,
    "inches": 0.0254,
    "cm": 0.01,
    "mm": 0.001,
    "yd": 0.9144,
}

_MASS_TO_KG = {
    "kg": 1.0,
    "kilogram": 1.0,
    "kilograms": 1.0,
    "g": 0.001,
    "gram": 0.001,
    "grams": 0.001,
    "lb": 0.45359237,
    "lbs": 0.45359237,
    "pound": 0.45359237,
    "pounds": 0.45359237,
    "oz": 0.028349523125,
    "ounce": 0.028349523125,
    "ounces": 0.028349523125,
}

_TEMP_UNITS = {"c", "celsius", "f", "fahrenheit", "k", "kelvin"}


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    src = from_unit.lower()
    dst = to_unit.lower()
    if src in {"c", "celsius"}:
        c = value
    elif src in {"f", "fahrenheit"}:
        c = (value - 32) * 5 / 9
    elif src in {"k", "kelvin"}:
        c = value - 273.15
    else:
        raise ValueError(f"unsupported temperature unit: {from_unit}")

    if dst in {"c", "celsius"}:
        return c
    if dst in {"f", "fahrenheit"}:
        return c * 9 / 5 + 32
    if dst in {"k", "kelvin"}:
        return c + 273.15
    raise ValueError(f"unsupported temperature unit: {to_unit}")


def _normalize_unit(unit: str) -> str:
    return unit.strip().lower().replace(" ", "")


async def unit_convert(value: float, from_unit: str, to_unit: str) -> ToolResult:
    try:
        val = float(value)
    except (TypeError, ValueError):
        return ToolResult(success=False, error="value must be a number")

    src = _normalize_unit(from_unit)
    dst = _normalize_unit(to_unit)
    if not src or not dst:
        return ToolResult(success=False, error="from_unit and to_unit are required")

    try:
        if src in _TEMP_UNITS or dst in _TEMP_UNITS:
            if src not in _TEMP_UNITS or dst not in _TEMP_UNITS:
                return ToolResult(success=False, error="temperature units cannot mix with length/mass")
            result = _convert_temperature(val, src, dst)
            category = "temperature"
        elif src in _LENGTH_TO_M and dst in _LENGTH_TO_M:
            meters = val * _LENGTH_TO_M[src]
            result = meters / _LENGTH_TO_M[dst]
            category = "length"
        elif src in _MASS_TO_KG and dst in _MASS_TO_KG:
            kg = val * _MASS_TO_KG[src]
            result = kg / _MASS_TO_KG[dst]
            category = "mass"
        else:
            return ToolResult(
                success=False,
                error="unsupported unit pair — use length, mass, or temperature units",
            )

        summary = f"{val} {from_unit} = {result:.6g} {to_unit} ({category})"
        return ToolResult(
            success=True,
            data={
                "value": val,
                "from_unit": from_unit,
                "to_unit": to_unit,
                "result": result,
                "category": category,
                "summary": summary,
            },
        )
    except ValueError as exc:
        return ToolResult(success=False, error=str(exc))
