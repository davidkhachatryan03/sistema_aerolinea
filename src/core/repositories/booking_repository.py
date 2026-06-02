from src.common import DBManager
from src.entities import Booking

class BookingRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def insert_booking(self, booking: Booking) -> None:
        self.db_manager.insert_rows("bookings", [booking])