import pytest
from datetime import datetime, date
from decimal import Decimal
from src.entities import *

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
def passenger_created(valid_passenger: dict) -> PassengerCreated:
    passenger_created = PassengerCreated(**valid_passenger)
    return passenger_created

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
def flight_created(valid_flight: dict) -> FlightCreated:
    flight_created = FlightCreated(**valid_flight)
    return flight_created

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
def document_created(valid_document: dict) -> DocumentCreated:
    document_created = DocumentCreated(**valid_document)
    return document_created

@pytest.fixture
def valid_booking() -> dict:
    return {
        "booking_reference": "ABC123",
        "booking_datetime": datetime(2026,1,1),
        "paid_amount_usd": Decimal("5000.25"),
        "current_status_id": 1
    }

@pytest.fixture
def booking_created(valid_booking: dict) -> BookingCreated:
    booking_created = BookingCreated(**valid_booking)
    return booking_created

@pytest.fixture
def valid_airplane() -> dict:
    return {
        "tail_number": "AB-1234",
        "manufacturer": "Airbus",
        "model": "A300-800",
        "capacity": 126,
        "range_km": 12000,
        "flight_hour_cost_usd": Decimal("1300.12"),
        "current_status_id": 1
    }

@pytest.fixture
def airplane_created(valid_airplane: dict) -> AirplaneCreated:
    airplane_created = AirplaneCreated(**valid_airplane)
    return airplane_created

@pytest.fixture
def valid_boarding_pass() -> dict:
    return {
        "issue_datetime": datetime(2026,1,1),
        "boarding_datetime": datetime(2026,1,1),
        "current_status_id": 1,
        "ticket_id": 1
    }

@pytest.fixture
def boarding_pass_created(valid_boarding_pass: dict) -> BoardingPassCreated:
    boarding_pass_created = BoardingPassCreated(**valid_boarding_pass)
    return boarding_pass_created

@pytest.fixture
def valid_route() -> dict:
    return {
        "flight_number": "AB123",
        "origin": "EZE",
        "destination": "CDG",
        "distance_km": 13000,
        "duration_min": 540
    }

@pytest.fixture
def route_created(valid_route: dict) -> RouteCreated:
    route_created = RouteCreated(**valid_route)
    return route_created

@pytest.fixture
def valid_ticket() -> dict:
    return {
        "ticket_number": "1234567890123",
        "paid_amount_usd": Decimal("1000.13"),
        "current_status_id": 1,
        "booking_id": 1,
        "flight_id": 1,
        "passenger_id": 1
    }

@pytest.fixture
def ticket_created(valid_ticket: dict) -> TicketCreated:
    ticket_created = TicketCreated(**valid_ticket)
    return ticket_created