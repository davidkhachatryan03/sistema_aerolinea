from src.core.repositories import PassengerRepository

class PassengerValidator:

    def __init__(self, passenger_repository: PassengerRepository) -> None:
        self.passenger_repository = passenger_repository 