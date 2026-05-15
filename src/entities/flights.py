from datetime import datetime
from decimal import Decimal

class FlightCreated:

    def __init__(self,
                scheduled_departure_datetime: datetime,
                scheduled_arrival_datetime: datetime,
                actual_departure_datetime: datetime,
                actual_arrival_datetime: datetime,
                operating_cost_usd: Decimal,
                base_price_usd: Decimal,
                current_status_id: int,
                route_id: int,
                airplane_id: int) -> None:
        
        self.scheduled_departure_datetime = scheduled_departure_datetime
        self.scheduled_arrival_datetime = scheduled_arrival_datetime
        self.actual_departure_datetime = actual_departure_datetime
        self.actual_arrival_datetime = actual_arrival_datetime
        self.operating_cost_usd = operating_cost_usd
        self.base_price_usd = base_price_usd
        self.current_status_id = current_status_id
        self.route_id = route_id
        self.airplane_id = airplane_id