from faker import Faker
from datetime import datetime, timedelta, date
import random
from typing import Any, cast
from src.DBManager import DBManager
from src.entidades.Pasajero import PasajeroBase, PasajeroDesdeDB
from src.entidades.Vuelo import VueloBase, VueloDesdeDB
from src.entidades.Venta import VentaBase, VentaDesdeDB
from src.entidades.TarjetaEmbarque import TarjetaEmbarqueBase, TarjetaEmbarqueDesdeDB
from src.entidades.Documento import DocumentoBase, DocumentoDesdeDB
from src.entidades.Ruta import RutaBase, RutaDesdeDB
from src.entidades.Avion import AvionBase, AvionDesdeDB
from src.entidades.AsignacionVuelo import AsignacionVueloBase, AsignacionVueloDesdeDB

class GeneradorDatos:

    def __init__(self, db_manager: DBManager) -> None:
        self.fake: Faker = Faker('es_AR')
        self.db_manager = db_manager

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
    
    def generar_asignaciones_vuelos(self, vuelos: list[VueloDesdeDB]) -> list[AsignacionVueloBase]:
        asignaciones: list[AsignacionVueloBase] = []

        for vuelo in vuelos:
            comandantes_disponibles: list[int] = self._obtener_personal_avion_disponibles(vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada, 1)
            copilotos_disponibles: list[int] = self._obtener_personal_avion_disponibles(vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada, 2)
            auxiliares_vuelo_disponibles: list[int] = self._obtener_personal_avion_disponibles(vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada, 3)
            supervisores_cabina_disponibles: list[int] = self._obtener_personal_avion_disponibles(vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada, 4)
            mecanicos_disponibles: list[int] = self._obtener_staff_disponibles(vuelo.fecha_partida_programada, 5)
            inspectores_disponibles: list[int] = self._obtener_staff_disponibles(vuelo.fecha_partida_programada, 6)
            agentes_disponibles: list[int] = self._obtener_staff_disponibles(vuelo.fecha_partida_programada, 7)
            supervisores_agentes_disponibles: list[int] = self._obtener_staff_disponibles(vuelo.fecha_partida_programada, 8)

            if not comandantes_disponibles:
                raise Exception("Error: no hay comandantes disponibles.")
            
            if not copilotos_disponibles:
                raise Exception("Error: no hay copilotos disponibles.")
            
            if not auxiliares_vuelo_disponibles:
                raise Exception("Error: no hay auxiliares de vuelo disponibles.")
            
            if not supervisores_cabina_disponibles:
                raise Exception("Error: no hay supervisores de cabina disponibles.")
            
            if not mecanicos_disponibles:
                raise Exception("Error: no hay mecánicos disponibles.")
            
            if not inspectores_disponibles:
                raise Exception("Error: no hay inspectores disponibles.")
            
            if len(agentes_disponibles) < 4:
                raise Exception("Error: no hay suficientes agentes disponibles.")
            
            if not supervisores_agentes_disponibles:
                raise Exception("Error: no hay supervisores de agentes disponibles.")
            
            fecha_inicio: datetime = vuelo.fecha_partida_programada - timedelta(hours=2)
            fecha_fin: datetime = vuelo.fecha_arribo_programada
            
            id_comandante: int = random.choice(comandantes_disponibles)
            asignacion_comandante = AsignacionVueloBase(fecha_inicio, fecha_fin, 1, vuelo.id, id_comandante)

            id_copiloto: int = random.choice(copilotos_disponibles)
            asignacion_copiloto = AsignacionVueloBase(fecha_inicio, fecha_fin, 2, vuelo.id, id_copiloto)

            id_auxiliar_vuelo: int = random.choice(auxiliares_vuelo_disponibles)
            asignacion_auxiliar_vuelo = AsignacionVueloBase(fecha_inicio, fecha_fin, 3, vuelo.id, id_auxiliar_vuelo)

            id_supervisor_cabina: int = random.choice(supervisores_cabina_disponibles)
            asignacion_supervisor_cabina = AsignacionVueloBase(fecha_inicio, fecha_fin, 4, vuelo.id, id_supervisor_cabina)
            
            fecha_fin: datetime = vuelo.fecha_arribo_programada

            id_mecanico: int = random.choice(mecanicos_disponibles)
            asingacion_mecanico = AsignacionVueloBase(fecha_inicio, fecha_fin, 8, vuelo.id, id_mecanico)

            id_inspector: int = random.choice(inspectores_disponibles)
            asignacion_inspector = AsignacionVueloBase(fecha_inicio, fecha_fin, 10, vuelo.id, id_inspector)

            for _ in range(2):
                id_agente: int = agentes_disponibles.pop()
                asignacion_agente = AsignacionVueloBase(fecha_inicio, fecha_fin, 5, vuelo.id, id_agente)
                asignaciones.append(asignacion_agente)
            
            for _ in range(2):
                id_agente: int = agentes_disponibles.pop()
                asignacion_agente = AsignacionVueloBase(fecha_inicio, fecha_fin, 6, vuelo.id, id_agente)
                asignaciones.append(asignacion_agente)

            asignaciones.extend([asignacion_comandante, asignacion_copiloto, asignacion_auxiliar_vuelo, asignacion_supervisor_cabina, asingacion_mecanico, asignacion_inspector])
        
        return asignaciones

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
    
    def _obtener_personal_avion_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime, id_cargo: int) -> list[int]:
        pilotos_disponibles: list[int] = []

        query = """
                SELECT  s.id
                FROM    staff s
                WHERE   s.id NOT IN (
                    SELECT  av.id_staff
                    FROM    asignaciones_vuelos av
                    JOIN    vuelos v 
                    ON      av.id_vuelo = v.id
                    WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                    AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                )
                AND     s.id IN (
                        SELECT  cs.id_staff
                        FROM    certificaciones_staff cs
                        WHERE   cs.licencia_hasta >= %s
                )
                AND     s.id_cargo_actual = %s
                AND     s.id_estado_actual = 1;
                """
        
        valores = (fecha_inicio, fecha_fin, fecha_fin, id_cargo)

        consulta_pilotos_disponibles: list[tuple] = self.db_manager.consultar(query, valores)

        for piloto in consulta_pilotos_disponibles:
            pilotos_disponibles.append(piloto[0])
        
        return pilotos_disponibles
    
    def _obtener_staff_disponibles(self, fecha_inicio: datetime, id_cargo: int) -> list[int]:
        staff_disponible: list[int] = []

        query = """
                SELECT  s.id
                FROM    staff s
                WHERE   s.id NOT IN (
                    SELECT  av.id_staff
                    FROM    asignaciones_vuelos av
                    JOIN    vuelos v ON av.id_vuelo = v.id
                    WHERE   DATE_SUB(v.fecha_partida_programada, INTERVAL 2 HOUR) < %s
                    AND     v.fecha_partida_programada > DATE_SUB(%s, INTERVAL 2 HOUR)
                )
                AND     s.id IN (
                        SELECT  cs.id_staff
                        FROM    certificaciones_staff cs
                        WHERE   cs.licencia_hasta >= %s
                )
                AND     s.id_cargo_actual = %s
                AND     s.id_estado_actual = 1
                """

        valores = (fecha_inicio, fecha_inicio, fecha_inicio, id_cargo)

        consulta_staff_disponible: list[tuple] = self.db_manager.consultar(query, valores)

        for staff in consulta_staff_disponible:
            staff_disponible.append(staff[0])

        return staff_disponible