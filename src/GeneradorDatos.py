from faker import Faker
from datetime import datetime, timedelta, date
import random
from typing import Any, cast
from src.entidades.Pasajero import PasajeroBase, PasajeroDesdeDB
from src.entidades.Vuelo import VueloBase, VueloDesdeDB
from src.entidades.Venta import VentaBase, VentaDesdeDB
from src.entidades.TarjetaEmbarque import TarjetaEmbarqueBase, TarjetaEmbarqueDesdeDB
from src.entidades.Documento import DocumentoBase, DocumentoDesdeDB
from src.entidades.Ruta import RutaBase, RutaDesdeDB
from src.entidades.Avion import AvionBase, AvionDesdeDB

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

    def generar_tarjetas_embarque(self, cant: int, ventas: list[VentaDesdeDB]) -> list[TarjetaEmbarqueBase]:
        tarjetas_de_embarque: list[TarjetaEmbarqueBase] = []

        for _ in range(cant):
            venta: VentaDesdeDB = random.choice(ventas)

            id_estado_actual: int = 1
            id_venta: int = venta.id

            tarjeta_embarque = TarjetaEmbarqueBase(id_estado_actual, id_venta)

            tarjetas_de_embarque.append(tarjeta_embarque)

        return tarjetas_de_embarque

    def generar_documentos(self, pasajeros: list[PasajeroDesdeDB]) -> list[DocumentoBase]:
        documentos: list[DocumentoBase] = []

        for pasajero in pasajeros:
            num_documento: str = self._generar_num_documento()
            fecha_vencimiento: date = self.fake.date_between(start_date="+180d", end_date="+10y")
            pais_emision: str = random.choices(["ARG","USA","ESP","BRA","CHL"], weights=[80,10,3,3,4])[0]
            id_pasajero: int = pasajero.id
            id_tipo_documento: int = random.choices([1,2,3], weights=[10,85,5])[0]

            documento = DocumentoBase(num_documento, fecha_vencimiento, pais_emision, id_pasajero, id_tipo_documento)

            documentos.append(documento)
        
        return documentos

    def generar_asignaciones_vuelos(self):
        pass

    def generar_vuelos(self, cant: int, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB]) -> list[VueloBase]:
        vuelos: list[VueloBase] = []

        for _ in range(cant):
            ruta: RutaDesdeDB = random.choice(rutas)
            avion: AvionDesdeDB = random.choice(aviones)

            fecha_partida_programada: datetime = self.fake.date_time_between(start_date="+30d", end_date="+180d")
            fecha_arribo_programada: datetime = fecha_partida_programada + timedelta(minutes=ruta.duracion_min)
            costo_operativo_usd: float = avion.costo_hora_vuelo * ruta.duracion_min / 60
            precio_venta_usd: float = costo_operativo_usd * 1.3
            id_ruta: int = ruta.id
            id_avion: int = avion.id
            id_estado_actual: int = 1

            vuelo = VueloBase(id_ruta, id_avion, id_estado_actual, fecha_arribo_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)

            vuelos.append(vuelo)

        return vuelos

    def _generar_num_reserva(self, longitud=6) -> str:
        num_reserva: str = ""

        caracteres = "23456789ABCDEFGHIJK"

        for _ in range(longitud):
            num_reserva += random.choice(caracteres)

        return num_reserva
    
    def _generar_num_documento(self, longitud=8) -> str:
        num_documento: str = ""

        numeros = "1234567890"

        for _ in range(longitud):
            num_documento += random.choice(numeros)

        return num_documento