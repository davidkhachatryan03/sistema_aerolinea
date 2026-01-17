from TablaManager import TablaManager
from DBManager import DBManager
from datetime import datetime
from typing import Any, cast
from src.entidades.Vuelo import Vuelo

FilaVuelo = tuple[datetime, datetime, int, int, int | None, datetime | None, datetime | None, float | None, float | None, int | None ]

class VuelosManager(TablaManager):

    def __init__(self, db_manager: DBManager):
        super().__init__("vuelos", db_manager)
    
    def registrar_vuelo(self, id_staff: int, vuelo:Vuelo) -> None:
        if not self._verificar_campos_requeridos(vuelo):
            raise Exception("Error: no se ingresaron todos los campos requeridos.")

        if not self._verificar_fechas(vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada):
            raise Exception("Error: la fecha de llegada debe ser posterior a la de partida.")

        if not self._verificar_avion(vuelo.id_avion, vuelo.id_ruta, vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada):
            raise Exception("Error: la ruta y avión seleccionados no son compatibles.")
        
        vuelo.id = None

        costo_operativo_usd: float = self._calcular_costo_operativo_usd(vuelo.id_ruta, vuelo.id_avion)
        
        precio_venta_usd: float = costo_operativo_usd * 1.30

        vuelo.costo_operativo_usd = costo_operativo_usd
        vuelo.precio_venta_usd = precio_venta_usd

        vuelo.id_estado_actual = 1

        datos: dict[str, Any] = vuelo.to_dict()

        super().agregar_fila(id_staff, datos)

    def modificar_fechas(self, id_vuelo: int, id_staff: int, fecha_partida_programada: datetime, fecha_arribo_programada: datetime) -> None:
        vuelo: Vuelo = self._obtener_vuelo(id_vuelo)

        if not self._verificar_fechas(fecha_partida_programada, fecha_arribo_programada):
            raise Exception("Error: la fecha de partida no puede ser mayor o igual a la fecha de llegada.")

        if not self._verificar_avion(vuelo.id_avion, vuelo.id_ruta, fecha_partida_programada, fecha_arribo_programada):
            raise Exception("Error: las fechas no son compatibles con el avión asignado.")

        super().modificar_fila(id_vuelo, id_staff, fecha_partida_programada=fecha_partida_programada, fecha_arribo_programada=fecha_arribo_programada)
    
    def modificar_avion(self, id_vuelo: int, id_staff: int, id_avion: int) -> None:
        vuelo: Vuelo = self._obtener_vuelo(id_vuelo)

        if vuelo.id_avion == id_avion:
            return

        if not self._verificar_avion(vuelo.id_avion, vuelo.id_ruta, vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada):
            raise Exception("Error: no es posible asignar el avión seleccionado.")
        
        super().modificar_fila(id_vuelo, id_staff, id_avion=id_avion)

    def modificar_ruta(self, id_vuelo: int, id_staff: int, id_ruta: int) -> None:
        vuelo: Vuelo = self._obtener_vuelo(id_vuelo)

        if vuelo.id_ruta == id_ruta:
            return

        if not self._verificar_avion(vuelo.id_avion, vuelo.id_ruta, vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada):
            raise Exception("Error: no es posible cambiar la ruta.")
        
        super().modificar_fila(id_vuelo, id_staff, id_ruta=id_ruta)

    def modificar_estado(self, id_vuelo: int, id_staff: int, id_estado_actual: int) -> None:
        vuelo: Vuelo = self._obtener_vuelo(id_vuelo)

        if vuelo.id_estado_actual == id_estado_actual:
            return
        
        estados_posibles = {
            1: "Programado",
            2: "En vuelo",
            3: "Aterrizado",
            4: "Cancelado"
        }

        if estados_posibles[id_estado_actual] == "En vuelo":
            fecha_partida_real: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            super().modificar_fila(id_vuelo, id_staff, id_estado_actual=id_estado_actual, fecha_partida_real=fecha_partida_real)
        elif estados_posibles[id_estado_actual] == "Aterrizado":
            fecha_arribo_real: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            super().modificar_fila(id_vuelo, id_staff, id_estado_actual=id_estado_actual, fecha_arribo_real=fecha_arribo_real)

    def _obtener_aviones_disponibles(self, id_ruta: int, fecha_partida_programada: datetime, fecha_arribo_programada: datetime) -> list[tuple[int]]:
        query = """
                SELECT  a.id
                FROM    aviones a
                WHERE   a.id NOT IN (
                    SELECT  v.id_avion
                    FROM    vuelos v
                    WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= %s
                    AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                )
                AND     a.autonomia_km > (
                        SELECT distancia_km 
                        FROM rutas 
                        WHERE id = %s
                )
                AND     a.id_estado_actual <> 3;
                """

        valores = (fecha_partida_programada, fecha_arribo_programada, id_ruta)

        aviones_disponibles: list[tuple[int]] = cast(list[tuple[int]], self.db_manager.consultar(query, valores))

        return aviones_disponibles

    def _verificar_fechas(self, fecha_partida_programada: datetime, fecha_arribo_programada: datetime) -> bool:
        if fecha_partida_programada < fecha_arribo_programada:
            return True
        
        return False

    def _verificar_avion(self, id_avion: int, id_ruta: int, fecha_partida_programada: datetime, fecha_arribo_programada: datetime) -> bool:
        id_aviones_disponibles: list[tuple[int]] = self._obtener_aviones_disponibles(id_ruta, fecha_partida_programada, fecha_arribo_programada)

        for id_avion_disponible in id_aviones_disponibles:
            if id_avion_disponible[0] == id_avion:
                return True

        return False

    def _calcular_costo_operativo_usd(self, id_ruta: int, id_avion: int) -> float:
        query: str = "SELECT duracion_min FROM rutas WHERE id = %s"
        consulta: list[tuple] = self.db_manager.consultar(query, (id_ruta,))
        
        if consulta:
            duracion_min: int = consulta[0][0]
        else:
            raise Exception("Error: no se encontró ningún resultado al consultar.")

        query = "SELECT costo_hora_vuelo FROM aviones WHERE id = %s"
        consulta: list[tuple] = self.db_manager.consultar(query, (id_avion,))

        if consulta:
            costo_hora_vuelo: float = consulta[0][0]
        else:
            raise Exception("Error: no se encontró ningún resultado al consultar.")

        return (duracion_min / 60) * costo_hora_vuelo

    def _obtener_vuelo(self, id_vuelo: int) -> Vuelo:
        query = """
                SELECT  fecha_partida_programada,
                        fecha_arribo_programada,
                        id_ruta,
                        id_avion,
                        id,
                        fecha_partida_real,
                        fecha_arribo_real,
                        costo_operativo_usd,
                        precio_venta_usd,
                        id_estado_actual                        
                FROM    vuelos 
                WHERE   id = %s
                """

        consulta_vuelo: FilaVuelo = self.db_manager.consultar(query, (id_vuelo,))[0]

        if consulta_vuelo:
            vuelo = Vuelo(*consulta_vuelo)
        else:
            raise Exception("Error: no se encontró ningún resultado al consultar.")

        return vuelo
    
    def _verificar_campos_requeridos(self, vuelo: Vuelo) -> bool:
        campos_requeridos = ["fecha_partida_programada", "fecha_arribo_programada", "id_ruta", "id_avion"]

        for campo in campos_requeridos:
            if getattr(vuelo, campo) == None:
                return False
        
        return True