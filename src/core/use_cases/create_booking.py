from src.core.units_of_work import CreateBookingUoW
from src.core.validators import BookingValidator, PassengerValidator, TicketValidator, DocumentValidator
from src.api.schemas import BookingRequest

class CreateBooking:

    def __init__(self,
                uow: CreateBookingUoW,
                booking_request: BookingRequest,
                booking_validator: BookingValidator,
                passenger_validator: PassengerValidator,
                ticket_validator: TicketValidator,
                document_validator: DocumentValidator) -> None:
        
        self.uow = uow
        self.booking_request = booking_request
        self.booking_validator = booking_validator
        self.passenger_validator = passenger_validator
        self.ticket_validator = ticket_validator
        self.document_validator = document_validator
    
    def process_booking(self) -> None:
        with self.uow:

            self.validate_passengers()
            self.validate_flights()

            self.insert_passengers()
            self.insert_booking()

    def validate_passengers(self) -> None:
        pass

    def validate_flights(self) -> None:
        pass

    def insert_booking(self) -> None:
        pass

    def insert_passengers(self) -> None:
        pass