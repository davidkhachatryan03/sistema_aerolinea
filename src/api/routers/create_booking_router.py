from fastapi import APIRouter, HTTPException
from src.api.schemas.booking_schema import BookingRequest, BookingResponse
from src.core.validators.flight_validator import FlightValidator
from src.common import DBManager
from src.common.exceptions import InvalidFlightId, InvalidPassengerId, InvalidPassengerBlacklisted, InvalidPaidAmountUsd
from src.core.use_cases import CreateBooking
from src.core.units_of_work import CreateBookingUoW

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse)
def create_booking(booking_request: BookingRequest):

    db_manager = DBManager()
    flight_validator = FlightValidator()
    booking_creator = CreateBooking(CreateBookingUoW(db_manager), flight_validator)

    booking_response: BookingResponse = booking_creator.execute(booking_request)

    return booking_response