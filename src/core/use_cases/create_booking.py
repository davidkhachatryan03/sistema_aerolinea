from src.core.units_of_work import CreateBookingUoW
from src.core.validators import BookingValidator, PassengerValidator, TicketValidator, DocumentValidator
from src.api.schemas import BookingRequest, PassengerRequest

class CreateBooking:

    def __init__(self,
                uow: CreateBookingUoW,
                booking_validator: BookingValidator,
                passenger_validator: PassengerValidator,
                ticket_validator: TicketValidator,
                document_validator: DocumentValidator) -> None:
        
        self.uow = uow
        self.booking_validator = booking_validator
        self.passenger_validator = passenger_validator
        self.ticket_validator = ticket_validator
        self.document_validator = document_validator
    
    def process_booking(self, booking_request: BookingRequest) -> None:
        with self.uow:

            self.insert_passengers(booking_request.passengers)

    def validate_passengers(self, passengers: list[PassengerRequest]) -> None:
        pass

    def validate_flights(self) -> None:
        pass

    def insert_booking(self) -> None:
        pass

    def insert_passengers(self) -> None:
        pass

    def insert_documents(self) -> None:
        pass