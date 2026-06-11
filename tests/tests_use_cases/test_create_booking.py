import pytest
from src.entities import Flight, Document, Passenger
from src.core.use_cases import CreateBooking, PassengerProcessor
from src.core.validators import FlightValidator, PassengerValidator
from src.api.schemas import BookingRequest, BookingResponse, PassengerRequest
from tests.tests_use_cases.fakes.fake_db_manager import FakeDBManager
from tests.tests_use_cases.fakes.fake_create_booking_uow import FakeCreateBookingUoW
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

def assert_booking_response(booking_response: BookingResponse, passengers_created: list[Passenger], flights_created: list[Flight], fake_uow: FakeCreateBookingUoW):
    assert len(fake_uow.passenger_repository.passengers) == len(passengers_created)
    assert len(fake_uow.document_repository.documents) == len(passengers_created)

    tickets: list[str] = booking_response.tickets
    paid_amount_usd: Decimal = (sum((flight.base_price_usd for flight in flights_created), Decimal("0")) * len(passengers_created)).quantize(Decimal("0.01"), ROUND_HALF_UP)

    assert booking_response.booking_reference == "ABC123"
    assert len(tickets) == len(passengers_created)

    for ticket in tickets:
        assert ticket == "1234567890123"
    
    assert isinstance(booking_response.booking_datetime, datetime)
    assert booking_response.paid_amount_usd == paid_amount_usd

def make_create_booking(fake_uow: FakeCreateBookingUoW) -> CreateBooking:
    return CreateBooking(
        uow=fake_uow,
        passenger_processor=PassengerProcessor(),
        flight_validator=FlightValidator(),
        passenger_validator=PassengerValidator(),
    )

@pytest.mark.usefixtures("fixed_booking_identifiers")
def test_create_booking_use_case_valid_input_passengers_registered(
    booking_request: BookingRequest, 
    flights_generated: list[Flight], 
    passengers_and_documents_generated: tuple[list[Passenger], list[Document]]
    ) -> None:

    fake_uow = FakeCreateBookingUoW(FakeDBManager())

    passengers_created: list[Passenger] 
    documents_created: list[Document] 
    passengers_created, documents_created = passengers_and_documents_generated

    fake_uow.flight_repository.insert_flights(flights_generated)
    fake_uow.passenger_repository.insert_passengers(passengers_created)
    fake_uow.document_repository.insert_documents(documents_created)

    assert len(fake_uow.passenger_repository.passengers) == len(passengers_created)
    assert len(fake_uow.document_repository.documents) == len(passengers_created)

    create_booking: CreateBooking = make_create_booking(fake_uow)

    booking_response: BookingResponse = create_booking.execute(booking_request)

    assert_booking_response(booking_response, passengers_created, flights_generated, fake_uow)

@pytest.mark.usefixtures("fixed_booking_identifiers")
def test_create_booking_use_case_valid_input_passengers_not_registered(
    booking_request: BookingRequest, 
    flights_generated: list[Flight], 
    passengers_and_documents_generated: tuple[list[Passenger], list[Document]]
    ) -> None:
    fake_uow = FakeCreateBookingUoW(FakeDBManager())

    passengers_created: list[Passenger] 
    documents_created: list[Document] 
    passengers_created, documents_created = passengers_and_documents_generated

    fake_uow.flight_repository.insert_flights(flights_generated)

    assert len(fake_uow.passenger_repository.passengers) == 0
    assert len(fake_uow.document_repository.documents) == 0

    create_booking: CreateBooking = make_create_booking(fake_uow)

    booking_response: BookingResponse = create_booking.execute(booking_request)

    assert_booking_response(booking_response, passengers_created, flights_generated, fake_uow)