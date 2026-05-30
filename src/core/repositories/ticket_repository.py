from src.common import DBManager
from src.entities import Ticket

class TicketRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def insert_tickets(self, tickets: list[Ticket]) -> None:
        self.db_manager.insert_rows("tickets", tickets)