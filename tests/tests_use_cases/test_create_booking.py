import pytest
from src.entities import Flight, Document, Passenger
from src.core.use_cases import CreateBooking, PassengerProcessor
from src.core.validators import FlightValidator, PassengerValidator
from src.api.schemas import BookingRequest, BookingResponse, PassengerRequest
from tests.tests_use_cases.fakes.fake_db_manager import FakeDBManager
from tests.tests_use_cases.fakes.fake_create_booking_uow import FakeCreateBookingUoW
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

def assert_booking_response(
    booking_response: BookingResponse, 
    passengers_created: list[Passenger], 
    flights_created: list[Flight], 
    fake_uow: FakeCreateBookingUoW,
    expected_booking_reference: str,
    expected_ticket_number: str
    ) -> None:
    assert len(fake_uow.passenger_repository.passengers) == len(passengers_created)

    tickets: list[str] = booking_response.tickets
    paid_amount_usd: Decimal = calculate_paid_amount_usd(flights_created, passengers_created)

    assert booking_response.booking_reference == expected_booking_reference
    assert len(tickets) == len(passengers_created)

    for ticket in tickets:
        assert ticket == expected_ticket_number
    
    assert isinstance(booking_response.booking_datetime, datetime)
    assert booking_response.paid_amount_usd == paid_amount_usd

def make_create_booking(fake_uow: FakeCreateBookingUoW) -> CreateBooking:
    return CreateBooking(
        uow=fake_uow,
        passenger_processor=PassengerProcessor(),
        flight_validator=FlightValidator(),
        passenger_validator=PassengerValidator(),
    )

def calculate_paid_amount_usd(flights_created: list[Flight], passengers_created: list[Passenger]) -> Decimal:
    return (sum((flight.base_price_usd for flight in flights_created), Decimal("0")) * len(passengers_created)).quantize(Decimal("0.01"), ROUND_HALF_UP)

@pytest.mark.usefixtures("fixed_booking_identifiers")
def test_create_booking_use_case_valid_input_passengers_registered(
    booking_request: BookingRequest, 
    flights_generated: list[Flight], 
    passengers_generated: list[Passenger],
    expected_booking_reference: str,
    expected_ticket_number: str
    ) -> None:

    assert len(booking_request.flights_id) > 0
    assert len(booking_request.passengers) > 0

    fake_uow = FakeCreateBookingUoW(FakeDBManager())

    fake_uow.flight_repository.insert_flights(flights_generated)
    fake_uow.passenger_repository.insert_passengers(passengers_generated)

    assert len(fake_uow.passenger_repository.passengers) == len(passengers_generated)

    create_booking: CreateBooking = make_create_booking(fake_uow)

    booking_response: BookingResponse = create_booking.execute(booking_request)

    assert_booking_response(booking_response, passengers_generated, flights_generated, fake_uow, expected_booking_reference, expected_ticket_number)

@pytest.mark.usefixtures("fixed_booking_identifiers")
def test_create_booking_use_case_valid_input_passengers_not_registered(
    booking_request: BookingRequest, 
    flights_generated: list[Flight], 
    passengers_generated: list[Passenger],
    expected_booking_reference: str,
    expected_ticket_number: str
    ) -> None:

    assert len(booking_request.flights_id) > 0
    assert len(booking_request.passengers) > 0

    fake_uow = FakeCreateBookingUoW(FakeDBManager())

    fake_uow.flight_repository.insert_flights(flights_generated)

    assert len(fake_uow.passenger_repository.passengers) == 0

    create_booking: CreateBooking = make_create_booking(fake_uow)

    booking_response: BookingResponse = create_booking.execute(booking_request)

    assert_booking_response(booking_response, passengers_generated, flights_generated, fake_uow, expected_booking_reference, expected_ticket_number)

@pytest.mark.usefixtures("fixed_booking_identifiers")
def test_create_booking_use_case_valid_input_passengers_registered_and_not_registered(
    booking_request: BookingRequest, 
    flights_generated: list[Flight], 
    passengers_generated: list[Passenger],
    expected_booking_reference: str,
    expected_ticket_number: str
    ) -> None:

    assert len(booking_request.flights_id) > 0
    assert len(booking_request.passengers) > 1

    fake_uow = FakeCreateBookingUoW(FakeDBManager())

    fake_uow.flight_repository.insert_flights(flights_generated)
    fake_uow.passenger_repository.insert_passengers([passengers_generated[0]])
    
    assert len(fake_uow.passenger_repository.passengers) == 1

    create_booking: CreateBooking = make_create_booking(fake_uow)

    booking_response: BookingResponse = create_booking.execute(booking_request)

    assert_booking_response(booking_response, passengers_generated, flights_generated, fake_uow, expected_booking_reference, expected_ticket_number)
