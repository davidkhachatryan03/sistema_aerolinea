from src.core.repositories import BookingRepository
from src.core.validators import BookingValidator
from src.entities import BookingCreated, BookingRetrieved

class BookingManager:

    def __init__(self, booking_repository: BookingRepository, booking_validator: BookingValidator) -> None:
        self.booking_repository = booking_repository
        self.booking_validator = booking_validator