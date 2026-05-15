import pytest
from src.entities import RouteCreated

def test_valid_route(valid_route: dict) -> None:
    route_created = RouteCreated(**valid_route)

    assert route_created.flight_number == valid_route["flight_number"]
    assert route_created.origin == valid_route["origin"]
    assert route_created.destination == valid_route["destination"]
    assert route_created.distance_km == valid_route["distance_km"]
    assert route_created.duration_min == valid_route["duration_min"]

@pytest.mark.parametrize("field, value, expected_exception", [
    ("flight_number", 123, TypeError),
    ("flight_number", "   ", ValueError),
    ("flight_number", "", ValueError),
    ("flight_number", "ABCDEFG", ValueError),
    ("origin", 123, TypeError),
    ("origin", "   ", ValueError),
    ("origin", "", ValueError),
    ("origin", "ABCDEFG", ValueError),
    ("destination", 123, TypeError),
    ("destination", "   ", ValueError),
    ("destination", "", ValueError),
    ("destination", "ABCDEFG", ValueError),
    ("distance_km", "123", TypeError),
    ("distance_km", 0, ValueError),
    ("distance_km", -100, ValueError),
    ("duration_min", "123", TypeError),
    ("duration_min", 0, ValueError),
    ("duration_min", -100, ValueError),
])

def test_invalid_route(valid_route: dict, field: str, value, expected_exception) -> None:
    test_data = valid_route.copy()
    test_data[field] = value

    with pytest.raises(expected_exception):
        RouteCreated(**test_data)