from fastapi import APIRouter
from src.api.schemas.booking_schema import BookingRequest, BookingResponse
from src.core.validators import FlightValidator, PassengerValidator
from src.common import DBManager
from src.core.use_cases import CreateBooking, PassengerProcessor
from src.core.units_of_work import CreateBookingUoW

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingResponse)
def create_booking(booking_request: BookingRequest):

    db_manager = DBManager()
    passenger_processor = PassengerProcessor()
    flight_validator = FlightValidator()
    passenger_validator = PassengerValidator()
    booking_creator = CreateBooking(CreateBookingUoW(db_manager), passenger_processor, flight_validator, passenger_validator)

    booking_response: BookingResponse = booking_creator.execute(booking_request)

    return booking_response