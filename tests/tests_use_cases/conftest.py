import pytest
from uuid import UUID
from src.entities import Passenger, Document, Flight
from src.api.schemas import BookingRequest, PassengerRequest
from datetime import datetime, date
from decimal import Decimal

@pytest.fixture
def booking_request() -> BookingRequest:
    return BookingRequest(
        flights_id=[UUID("019eb14c-ed68-7e52-a495-8a80b519a12f")], 
        passengers=[
            PassengerRequest(
            full_name="David Khachatryan",
            birth_date=date(2000,1,1),
            email="email@example.com",
            phone_number="1234567890",
            document_number="AA123456",
            valid_from=date(2023,1,1),
            valid_until=date(2033,1,1),
            issue_country="ARG",
            document_type_id=1
        ),
            PassengerRequest(
            full_name="John Doe",
            birth_date=date(1980,1,1),
            email="jhon@example.com",
            phone_number="9876543210",
            document_number="BB654321",
            valid_from=date(2025,1,1),
            valid_until=date(2035,1,1),
            issue_country="USA",
            document_type_id=1
        )
        ]
    )

@pytest.fixture
def passengers_and_documents_generated(booking_request: BookingRequest) -> tuple[list[Passenger], list[Document]]:
    documents: list[Document] = []
    passengers: list[Passenger] = []

    passengers_requested: list[PassengerRequest] = booking_request.passengers

    for passenger in passengers_requested:
        
        passenger_created = Passenger.new_passenger(
            full_name=passenger.full_name,
            birth_date=passenger.birth_date,
            email=passenger.email,
            phone_number=passenger.phone_number
            )

        document_created = Document.new_document(
            document_number=passenger.document_number,
            valid_from=passenger.valid_from,
            valid_until=passenger.valid_until,
            issue_country=passenger.issue_country,
            passenger_id=passenger_created.id,
            document_type_id=1
        )

        passengers.append(passenger_created)
        documents.append(document_created)
    
    return passengers, documents

@pytest.fixture
def flights_generated(booking_request: BookingRequest) -> list[Flight]:
    flights: list[Flight] = []
    flights_id: list[UUID] = booking_request.flights_id

    for id in flights_id:
        flight = Flight.new_flight(
            scheduled_departure_datetime=datetime(2025,1,1),
            scheduled_arrival_datetime=datetime(2025,1,2),
            operating_cost_usd=Decimal("10000.78"),
            route_id=1,
            airplane_id=1
        )

        flight.id = id

        flights.append(flight)
    
    return flights

@pytest.fixture
def fixed_booking_identifiers(mocker):
    mocker.patch(
        "src.entities.Booking._generate_reference",
        return_value="ABC123"
    )

    mocker.patch(
        "src.entities.Ticket._generate_ticket_number",
        return_value="1234567890123"
    )