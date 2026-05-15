from src.core.repositories import BookingRepository
from src.core.validators import BookingValidator

class BookingManager:

    def __init__(self, booking_repository: BookingRepository, booking_validator: BookingValidator) -> None:
        self.booking_repository = booking_repository
        self.booing_validator = self.booing_validator