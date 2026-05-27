from src.core.repositories import PassengerRepository
from src.api.schemas import PassengerRequest

class PassengerValidator:

    def __init__(self, passenger_repository: PassengerRepository) -> None:
        self.passenger_repository = passenger_repository