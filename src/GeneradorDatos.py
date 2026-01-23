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

    def generar_pasajeros(self, cant: int) -> list[PasajeroBase]:
        pasajeros: list[PasajeroBase] = []
        
        for _ in range(cant):
            nombre_completo: str = self.fake.name()
            email: str = self.fake.email()
            telefono: str = self.fake.numerify("11%#######")
            esta_en_lista_negra: bool = random.choices([True, False], weights=[3, 97])[0]
            es_vip: bool = random.choices([True, False], weights=[20, 80])[0]

            pasajero = PasajeroBase(nombre_completo, email, telefono, esta_en_lista_negra, es_vip)

            pasajeros.append(pasajero)

        return pasajeros


    def generar_ventas(self):
        pass

    def generar_tarjetas_embarque(self):
        pass

    def generar_documentos(self):
        pass

    def generar_asignaciones_vuelos(self):
        pass