from src.common import DBManager
from src.entities import Passenger
from src.api.schemas import PassengerRequest
from uuid import UUID

class PassengerRepository:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager

    def insert_passengers(self, passengers: list[Passenger]) -> None:
        self.db_manager.insert_rows("passengers", passengers)

    def retrieve_passengers_by_id(self, passengers_id: list[UUID]) -> list[Passenger]:
        if not passengers_id:
            return []
        
        placeholders = ",".join(["%s" * len(passengers_id)])

        query = """
                SELECT  *
                FROM    passengers
                WHERE   id IN ({})
                """.format(placeholders)
        
        values = passengers_id

        result: list[tuple] = self.db_manager.retrieve(query, values)

        if result:
            return [Passenger(*row) for row in result]
        
        return []