from faker import Faker
from datetime import datetime, timedelta, date
import random
from typing import Any, cast

class GeneradorDatos:

    def __init__(self) -> None:
        self.fake: Faker = Faker('es_AR')

    def generar_pasajeros(self):
        pass

    def generar_ventas(self):
        pass

    def generar_tarjetas_embarque(self):
        pass

    def generar_documentos(self):
        pass

    def generar_asignaciones_vuelos(self):
        pass