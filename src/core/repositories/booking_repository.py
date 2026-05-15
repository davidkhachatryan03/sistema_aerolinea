from common import DBManager
from common.queries import RETRIEVE_BOOKING_REFERENCE
from common.rows import BookingRow
from entities import BookingCreated, BookingRetrieved

class BookingRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def retrieve_booking(self, booking_reference: str) -> BookingRetrieved:
        row: BookingRow = self.db_manager.retrieve(query=RETRIEVE_BOOKING_REFERENCE, values=(booking_reference,))[0]
        booking_retrieved = BookingRetrieved(id=row[0],
                                            booking_reference=row[1],
                                            booking_datetime=row[2],
                                            paid_amount_usd=row[3],
                                            current_status_id=row[4])

        return booking_retrieved