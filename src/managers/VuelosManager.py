from typing import Any, cast
from datetime import datetime
from decimal import Decimal
from src.tipos import FilaVuelo
from src.managers.DBManager import DBManager
from src.managers.TablaManager import TablaManager
from src.entidades import VueloBase, VueloDesdeDB
from src.querys import OBTENER_VUELO, OBTENER_AVIONES

class VuelosManager(TablaManager):

    def __init__(self, db_manager: DBManager):
        super().__init__("vuelos", db_manager)
        self.campos_requeridos = ["fecha_partida_programada", "fecha_arribo_programada", "id_ruta", "id_avion"]
        self.estados_posibles = {
            1: "Programado",
            2: "En vuelo",
            3: "Aterrizado",
            4: "Cancelado"
        }
    
    def registrar_vuelo(self, id_staff: int, vuelo: VueloBase) -> None:
        if not self._verificar_campos_requeridos(vuelo):
            raise Exception("Error: no se ingresaron todos los campos requeridos.")

        if not self._verificar_fechas(vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada):
            raise Exception("Error: la fecha de llegada debe ser posterior a la de partida.")

        if not self._verificar_avion(vuelo.id_avion, vuelo.id_ruta, vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada):
            print("Error: la ruta y avión seleccionados no son compatibles.\n")
            return

        costo_operativo_usd: Decimal = self._calcular_costo_operativo_usd(vuelo.id_ruta, vuelo.id_avion)
        
        precio_venta_usd: Decimal = costo_operativo_usd * Decimal(1.30)

        vuelo.costo_operativo_usd = costo_operativo_usd
        vuelo.precio_venta_usd = precio_venta_usd

        vuelo.id_estado_actual = 1

        datos: dict[str, Any] = vuelo.to_dict()

        super().agregar_fila(id_staff, datos)

    def modificar_fechas(self, id_vuelo: int, id_staff: int, fecha_partida_programada: datetime, fecha_arribo_programada: datetime) -> None:
        vuelo: VueloDesdeDB = self._obtener_vuelo(id_vuelo)

        if vuelo.fecha_partida_programada == fecha_partida_programada or vuelo.fecha_arribo_programada == fecha_arribo_programada:
            return

        if not super()._verificar_id_a_modificar(id_vuelo):
            raise Exception("Error: el id a modificar no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")

        if not self._verificar_fechas(fecha_partida_programada, fecha_arribo_programada):
            raise Exception("Error: la fecha de partida no puede ser mayor o igual a la fecha de llegada.")

        if not self._verificar_avion(vuelo.id_avion, vuelo.id_ruta, fecha_partida_programada, fecha_arribo_programada):
            raise Exception("Error: las fechas no son compatibles con el avión asignado.")

        super().modificar_fila(id_vuelo, id_staff, fecha_partida_programada=fecha_partida_programada, fecha_arribo_programada=fecha_arribo_programada)
    
    def modificar_avion(self, id_vuelo: int, id_staff: int, id_avion: int) -> None:
        vuelo: VueloDesdeDB = self._obtener_vuelo(id_vuelo)

        if vuelo.id_avion == id_avion:
            return
        
        if not super()._verificar_id_a_modificar(id_vuelo):
            raise Exception("Error: el id a modificaro no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")

        if not self._verificar_avion(vuelo.id_avion, vuelo.id_ruta, vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada):
            raise Exception("Error: no es posible asignar el avión seleccionado.")
        
        super().modificar_fila(id_vuelo, id_staff, id_avion=id_avion)

    def modificar_ruta(self, id_vuelo: int, id_staff: int, id_ruta: int) -> None:
        vuelo: VueloDesdeDB = self._obtener_vuelo(id_vuelo)

        if vuelo.id_ruta == id_ruta:
            return
        
        if not super()._verificar_id_a_modificar(id_vuelo):
            raise Exception("Error: el id a modificaro no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")

        if not self._verificar_avion(vuelo.id_avion, vuelo.id_ruta, vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada):
            raise Exception("Error: no es posible cambiar la ruta.")
        
        super().modificar_fila(id_vuelo, id_staff, id_ruta=id_ruta)

    def modificar_estado(self, id_vuelo: int, id_staff: int, id_estado_actual: int) -> None:
        vuelo: VueloDesdeDB = self._obtener_vuelo(id_vuelo)

        if not super()._verificar_id_a_modificar(id_vuelo):
            raise Exception("Error: el id a modificaro no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")

        if vuelo.id_estado_actual == id_estado_actual:
            return

        if self.estados_posibles[id_estado_actual] == "En vuelo":
            fecha_partida_real: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            super().modificar_fila(id_vuelo, id_staff, id_estado_actual=id_estado_actual, fecha_partida_real=fecha_partida_real)
        elif self.estados_posibles[id_estado_actual] == "Aterrizado":
            fecha_arribo_real: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            super().modificar_fila(id_vuelo, id_staff, id_estado_actual=id_estado_actual, fecha_arribo_real=fecha_arribo_real)

    def _obtener_aviones_disponibles(self, id_ruta: int, fecha_partida_programada: datetime, fecha_arribo_programada: datetime) -> list[int]:
        query = OBTENER_AVIONES

        valores = (fecha_partida_programada, fecha_arribo_programada, id_ruta)

        aviones_disponibles: list[int] = self.db_manager.consultar_columna_unica(query, valores)

        return aviones_disponibles

    def _verificar_fechas(self, fecha_partida_programada: datetime, fecha_arribo_programada: datetime) -> bool:
        if fecha_partida_programada < fecha_arribo_programada:
            return True
        
        return False

    def _verificar_avion(self, id_avion: int, id_ruta: int, fecha_partida_programada: datetime, fecha_arribo_programada: datetime) -> bool:
        id_aviones_disponibles: list[int] = self._obtener_aviones_disponibles(id_ruta, fecha_partida_programada, fecha_arribo_programada)

        for id_avion_disponible in id_aviones_disponibles:
            if id_avion_disponible == id_avion:
                return True

        return False

    def _calcular_costo_operativo_usd(self, id_ruta: int, id_avion: int) -> Decimal:
        query: str = "SELECT duracion_min FROM rutas WHERE id = %s"
        consulta_duracion_min: list[int] = self.db_manager.consultar_columna_unica(query, (id_ruta,))
        
        if not consulta_duracion_min:
            raise Exception("Error: no se encontró ningún resultado al consultar.")
        
        duracion_min: int = consulta_duracion_min[0]

        query = "SELECT costo_hora_vuelo FROM aviones WHERE id = %s"
        consulta_costo_hora_vuelo: list[int] = self.db_manager.consultar_columna_unica(query, (id_avion,))

        if not consulta_costo_hora_vuelo:
            raise Exception("Error: no se encontró ningún resultado al consultar.")
        
        costo_hora_vuelo: int = consulta_costo_hora_vuelo[0]

        return (duracion_min / Decimal("60")) * costo_hora_vuelo

    def _obtener_vuelo(self, id_vuelo: int) -> VueloDesdeDB:
        query = OBTENER_VUELO

        consulta_vuelo: list[tuple] = self.db_manager.consultar(query, (id_vuelo,))

        if consulta_vuelo:
            fila_vuelo: FilaVuelo = consulta_vuelo[0]
            vuelo = VueloDesdeDB(*fila_vuelo)
        else:
            raise Exception("Error: no se encontró ningún resultado al consultar.")

        return vuelo
    
    def _verificar_campos_requeridos(self, vuelo: VueloBase) -> bool:
        for campo in self.campos_requeridos:
            if getattr(vuelo, campo) == None:
                return False
        
        return True