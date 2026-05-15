import pytest
from datetime import datetime, date
from decimal import Decimal

@pytest.fixture
def valid_passenger() -> dict:
    return {
        "full_name": "David Khachatryan",
        "email": "email@test.com",
        "phone_number": 1143254683,
        "is_blacklisted": False,
        "is_vip": True
    }

@pytest.fixture
def valid_flight() -> dict:
    return {
        "scheduled_departure_datetime": datetime(2026,1,1),
        "scheduled_arrival_datetime": datetime(2026,1,2),
        "operating_cost_usd": Decimal("10000.13"),
        "base_price_usd": Decimal("20000.14"),
        "current_status_id": 1,
        "route_id": 1,
        "airplane_id": 1
    }

@pytest.fixture
def valid_document() -> dict:
    return {
        "document_number": "ABC123456",
        "valid_from": date(2025,1,1),
        "valid_until": date(2035,1,1),
        "issue_country": "ARG",
        "passenger_id": 1,
        "document_type_id": 1
    }

@pytest.fixture
def valid_booking() -> dict:
    return {
        "booking_reference": "ABC123",
        "booking_datetime": datetime(2026,1,1),
        "paid_amount_usd": Decimal("5000.25"),
        "current_status_id": 1
    }