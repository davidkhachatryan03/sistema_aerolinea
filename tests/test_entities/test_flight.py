import pytest
from src.entities import FlightCreated
from decimal import Decimal

def test_valid_flight(valid_flight: dict) -> None:
    flight_created = FlightCreated(**valid_flight)

    assert flight_created.scheduled_departure_datetime == valid_flight["scheduled_departure_datetime"]
    assert flight_created.scheduled_arrival_datetime == valid_flight["scheduled_arrival_datetime"]
    assert flight_created.operating_cost_usd == valid_flight["operating_cost_usd"]
    assert flight_created.base_price_usd == valid_flight["base_price_usd"]
    assert flight_created.current_status_id == valid_flight["current_status_id"]
    assert flight_created.route_id == valid_flight["route_id"]
    assert flight_created.airplane_id == valid_flight["airplane_id"]

@pytest.mark.parametrize("field, value, expected_exception", [
    ("scheduled_departure_datetime", 123, TypeError),
    ("scheduled_arrival_datetime", 123, TypeError),
    ("operating_cost_usd", "123", TypeError),
    ("operating_cost_usd", Decimal("0"), ValueError),
    ("operating_cost_usd", Decimal("-100"), ValueError),
    ("base_price_usd", "123", TypeError),
    ("base_price_usd", Decimal("0"), ValueError),
    ("base_price_usd", Decimal("-100"), ValueError),
    ("current_status_id", "123", TypeError),
    ("current_status_id", 0, ValueError),
    ("current_status_id", -100, ValueError),
    ("route_id", "123", TypeError),
    ("route_id", 0, ValueError),
    ("route_id", -100, ValueError),
    ("airplane_id", "123", TypeError),
    ("airplane_id", 0, ValueError),
    ("airplane_id", -100, ValueError),
])

def test_invalid_flight(valid_flight: dict, field: str, value, expected_exception) -> None:
    test_data = valid_flight.copy()
    test_data[field] = value

    with pytest.raises(expected_exception):
        FlightCreated(**test_data)