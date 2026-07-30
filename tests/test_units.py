import pytest

from pocket_agent.tools.util.units import unit_convert


@pytest.mark.asyncio
async def test_unit_convert_miles_to_km():
    result = await unit_convert(1.0, "miles", "km")
    assert result.success
    assert result.data["category"] == "length"
    assert 1.5 < result.data["result"] < 1.7


@pytest.mark.asyncio
async def test_unit_convert_fahrenheit_to_celsius():
    result = await unit_convert(32.0, "fahrenheit", "celsius")
    assert result.success
    assert abs(result.data["result"]) < 0.01
