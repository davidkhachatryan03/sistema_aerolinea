from repositories import BookingRepository
from src.entities import BookingCreated

class BookingValidator:

    def __init__(self, booking_repository: BookingRepository) -> None:
        self.booking_repository = booking_repository