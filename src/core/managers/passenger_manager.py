from src.core.repositories import PassengerRepository
from src.core.validators import PassengerValidator

class PassengerManager:

    def __init__(self, passenger_repository: PassengerRepository, passenger_validator: PassengerValidator) -> None:
        self.passenger_repository = passenger_repository
        self.passenger_validator = passenger_validator