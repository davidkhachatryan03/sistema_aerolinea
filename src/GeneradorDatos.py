from faker import Faker
from datetime import datetime, timedelta, date
from DBManager import DBManager
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from typing import Any, cast
import random

class GeneradorDatos:

    def __init__(self, db_manager: DBManager) -> None:
        self.fake: Faker = Faker('es_AR')
        self.db_manager: DBManager = db_manager
        self.cursor: MySQLCursor | None = db_manager.obtener_cursor()
        self.conexion: MySQLConnection | None = db_manager.obtener_conexion()

    def generar_pasajeros(self, cant: int) -> list[tuple]:
        pasajeros: list[tuple[str, str, str, int, int ]] = []

        for _ in range(cant):
            pasajero: tuple[str, str, str, int , int] = (
                f"{self.fake.first_name()} {self.fake.last_name()}",
                self.fake.email(),
                self.fake.numerify("%#########"),
                0,
                0
            )

            pasajeros.append(pasajero)

        return pasajeros

    def generar_vuelos(self, cant: int) -> list[tuple[date, date, None, None, float, float, float, int, int, int]] | None:
        if self.cursor == None or self.conexion == None:
                print("No hay cursor.")
                return
        
        vuelos: list[tuple[date, date, None, None, float, float, float, int, int, int]] = []

        self.cursor.execute("SELECT * FROM aviones")
        aviones: list[tuple[int, str, str, str, int, int, float, int]] = cast(list[tuple[int, str, str, str, int, int, float, int]], self.cursor.fetchall())

        self.cursor.execute("SELECT * FROM rutas")
        rutas: list[tuple[int, str, str, str, int, int]] = cast(list[tuple[int, str, str, str, int, int]], self.cursor.fetchall())

        for _ in range(cant):
            ruta: tuple[int, str, str, str, int, int] = random.choice(rutas)
            distancia_km: int = ruta[5]

            fecha_partida_programada: date = self.fake.date_between(start_date="+30d", end_date="+180d")
            duracion_vuelo: timedelta = timedelta(minutes=ruta[5])
            fecha_arribo_programada: date = fecha_partida_programada + duracion_vuelo

            avion: tuple = random.choice(aviones)
            autonomia_km: int = avion[5]

            while autonomia_km < distancia_km:
                avion = random.choice(aviones)

            costo_operativo_usd: float = avion[6] * ruta[5] / 60

            precio_venta_usd: float = costo_operativo_usd * 1.30

            vuelo = (
                fecha_partida_programada,
                fecha_arribo_programada,
                None,
                None,
                avion[6] * ruta[5] / 60,
                costo_operativo_usd,
                precio_venta_usd,
                ruta[0],
                avion[0],
                1
            )

            vuelos.append(vuelo)
        
        return vuelos

    def generar_ventas(self, pasajeros, vuelos, cant):
        ventas = []

        for _ in range(cant):
            num_reserva = self.fake.bothify("??####", letters="ABCDEFGHIJKLMN")
            fecha_venta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            vuelo = random.choice(vuelo)

            venta = (
                num_reserva,
                fecha_venta,


            )