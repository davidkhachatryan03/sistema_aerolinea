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

    def generar_ventas(self, cant: int, vuelos: list[VueloDesdeDB], pasajeros: list[PasajeroDesdeDB]) -> list[VentaBase]:
        ventas: list[VentaBase] = []

        for _ in range(cant):
            pasajero: PasajeroDesdeDB = random.choice(pasajeros)
            vuelo: VueloDesdeDB = random.choice(vuelos)

            id_pasajero: int = pasajero.id
            id_vuelo: int = vuelo.id
            num_reserva: str = self._generar_num_reserva()
            precio_pagado_usd: float = vuelo.precio_venta_usd
            id_estado_actual: int = random.choices([1,2,3,4], weights=[70,10,15,5])[0]

            venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

            ventas.append(venta)

        return ventas

    def generar_tarjetas_embarque(self):
        pass

    def generar_documentos(self):
        pass

    def generar_asignaciones_vuelos(self):
        pass

    def generar_vuelos(self):
        pass

    def _generar_num_reserva(self, longitud=6) -> str:
        num_reserva: str = ""

        caracteres = "23456789ABCDEFGHIJK"

        for _ in range(longitud):
            num_reserva += random.choice(caracteres)

        return num_reserva