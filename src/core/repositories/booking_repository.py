from typing import cast
from common import DBManager
from common.rows import BookingRow
from entities import BookingCreated, BookingRetrieved

class BookingRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager  