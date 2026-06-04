import pytest
from src.entities import Booking, Flight
from decimal import Decimal
from uuid import UUID
from datetime import datetime

@pytest.fixture
def booking() -> Booking:
    return Booking(
        id=UUID("019e92b3-e0db-7244-a9a2-43322a076e75"),
        booking_reference="ABC123",
        booking_datetime=datetime(2026, 1, 1),
        paid_amount_usd=Decimal("10000.76"),
        current_status_id=1
    )

@pytest.fixture
def flight() -> Flight:
    return Flight(
        id=UUID("019e92b3-e0db-7244-a9a2-43322a076e75"),
        scheduled_departure_datetime=datetime(2026, 1, 1),
        scheduled_arrival_datetime=datetime(2026, 1, 2),
        actual_departure_datetime=datetime(2026, 1, 1),
        actual_arrival_datetime=datetime(2026, 1, 2),
        operating_cost_usd=Decimal("10000"),
        base_price_usd=Decimal("13000"),
        current_status_id=1,
        route_id=1,
        airplane_id=1
    )