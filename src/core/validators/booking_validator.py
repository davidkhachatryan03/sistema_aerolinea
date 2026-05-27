from src.core.repositories import BookingRepository
from src.api.schemas import BookingRequest
from uuid import UUID
from decimal import Decimal
from src.entities import Passenger, Flight
from src.common.exceptions import InvalidPassengerBlacklisted, InvalidPassengerId ,InvalidFlightId, InvalidPaidAmountUsd

class BookingValidator:

    def __init__(self, booking_repository: BookingRepository) -> None:
        self.booking_repository = booking_repository