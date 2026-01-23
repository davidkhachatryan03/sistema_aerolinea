from faker import Faker
from datetime import datetime, timedelta, date
import random
from typing import Any, cast
from src.entidades.Pasajero import PasajeroBase, PasajeroDesdeDB
from src.entidades.Vuelo import VueloBase, VueloDesdeDB
from src.entidades.Venta import VentaBase, VentaDesdeDB

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