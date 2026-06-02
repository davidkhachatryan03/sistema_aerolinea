import os, uuid6, random
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID
from src.common import DBManager
from faker import Faker
from src.entities import Passenger, Document, Flight, RouteRetrieved, AirplaneRetrieved

class DataSeeder:

    def __init__(self, db_manager: DBManager) -> None:
        self.db_manager = db_manager
        self.faker = Faker()
    
    def execute(self) -> None:
        with self.db_manager as db_manager:
            db_manager.execute_sql_file(os.path.join(os.getcwd(), "sql", "delete_data.sql"))
            self.execute_sql_files(db_manager)
            self.insert_passengers_and_documents(db_manager)
            self.insert_flights(db_manager)

    def execute_sql_files(self, db_manager: DBManager) -> None:
        cwd: str = os.getcwd()
        sql_insert_files_route: str = os.path.join(cwd, "sql", "inserts")
        sql_insert_files: list[str] = sorted(os.listdir(sql_insert_files_route))

        for file in sql_insert_files:
            file_route: str = os.path.join(sql_insert_files_route, file)
            db_manager.execute_sql_file(file_route)

    def insert_passengers_and_documents(self, db_manager: DBManager, cant=100) -> None:
        passengers: list[Passenger] = []
        documents: list[Document] = []
        
        for _ in range(cant):
            passenger = Passenger.new_passenger(
                full_name=self.faker.name(),
                birth_date=self.faker.date_between(start_date="-50y", end_date="-5y"),
                email=self.faker.email(),
                phone_number=str(self.faker.numerify(text="%#########"))
            )

            valid_from = self.faker.date_between(start_date=passenger.birth_date + timedelta(days=365))
            valid_until = valid_from + timedelta(days=1825)

            document = Document.new_document(
                document_number=self.faker.bothify(text="??########", letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                valid_from=valid_from,
                valid_until=valid_until,
                issue_country=random.choices(["ARG", "ESP", "BRA", "ITA", "URY", "CHL", "USA"], weights=[40, 15, 15, 10, 10, 5, 5])[0],
                passenger_id=passenger.id,
                document_type_id=1
            )

            passengers.append(passenger)
            documents.append(document)
        
        db_manager.insert_rows("passengers", passengers)
        db_manager.insert_rows("documents", documents)
    
    def insert_flights(self, db_manager: DBManager, cant=100) -> None:
        flights: list[Flight] = []
        routes: list[RouteRetrieved] = [RouteRetrieved(*route) for route in db_manager.retrieve("SELECT * FROM routes")]
        airplanes: list[AirplaneRetrieved] = [AirplaneRetrieved(*airplane) for airplane in db_manager.retrieve("SELECT * FROM airplanes")]

        for _ in range(cant):
            flag = True

            while flag:
                route: RouteRetrieved = random.choice(routes)
                airplane: AirplaneRetrieved = random.choice(airplanes)

                if route._distance_km < airplane.range_km:
                    flag = False

            scheduled_departure_datetime: datetime = self.faker.date_time_between(start_date="+30d", end_date="+180d")
            scheduled_arrival_datetime: datetime = scheduled_departure_datetime + timedelta(minutes=route.duration_min)

            operating_cost_usd: Decimal = airplane.flight_hour_cost_usd * (Decimal(route.duration_min) / Decimal("60")).quantize(Decimal("0.01"), ROUND_HALF_UP)

            flight = Flight(
                id=uuid6.uuid7(),
                scheduled_departure_datetime=scheduled_departure_datetime,
                scheduled_arrival_datetime=scheduled_arrival_datetime,
                actual_departure_datetime=None,
                actual_arrival_datetime=None,
                operating_cost_usd=operating_cost_usd,
                base_price_usd=(operating_cost_usd * Decimal("1.30")).quantize(Decimal("0.01"), ROUND_HALF_UP),
                current_status_id=1,
                route_id=route.id,
                airplane_id=airplane.id
            )

            flights.append(flight)
        
        db_manager.insert_rows("flights", flights)