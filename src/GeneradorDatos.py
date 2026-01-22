from faker import Faker
from datetime import datetime, timedelta, date
import random
from typing import Any, cast
from src.entidades.Pasajero import Pasajero
from src.entidades.Vuelo import Vuelo
from src.entidades.Venta import Venta

FilaPasajero = tuple[str, str, int, bool, bool]
FilaVenta = tuple[int, int, str | None, datetime | None, float | None, int | None, int | None]

class GeneradorDatos:

    def __init__(self) -> None:
        self.fake: Faker = Faker('es_AR')

    def generar_pasajeros(self, cant: int) -> list[Pasajero]:
        pasajeros: list[Pasajero] = []

        for _ in range(cant):
            nombre_completo: str = self.fake.name()
            email: str = self.fake.email()
            telefono: int = int(self.fake.numerify("11%#######"))
            esta_en_lista_negra: bool = True
            es_vip: bool = False

            fila_pasajero: FilaPasajero = (nombre_completo, email, telefono, esta_en_lista_negra, es_vip)
            pasajero = Pasajero(*fila_pasajero)
            pasajeros.append(pasajero)

        return pasajeros

    def generar_ventas(self, pasajeros: list[Pasajero], vuelos: list[Vuelo]):
        ventas: list[Venta] = []

        for _ in range(len(pasajeros)):
            pasajero: Pasajero = random.choice(pasajeros)
            vuelo: Vuelo = random.choice(vuelos)

            num_reserva: str = self.fake.bothify("??##?#")
            precio_pagado_usd: float | None = vuelo.precio_venta_usd
            id_vuelo: int = vuelo.id
            id_estado_actual: int = 1
            id_pasajero: int = pasajero.id

            fila_venta: FilaVenta = (id_pasajero, id_vuelo, )

    def generar_tarjetas_embarque(self):
        pass

    def generar_documentos(self):
        pass

    def generar_asignaciones_vuelos(self):
        pass