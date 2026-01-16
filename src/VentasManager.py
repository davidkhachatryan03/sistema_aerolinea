from TablaManager import TablaManager
from datetime import datetime
from typing import Any
from collections.abc import Iterable
import random

FilaVenta = tuple[int, int, int | None, str | None, datetime | None, float | None, int | None]

class Venta:

    def __init__(self, id_pasajero: int, id_vuelo: int, id: int | None, num_reserva: str | None=None, fecha_venta: datetime | None=None, precio_pagado_usd: float | None=None, id_estado_actual: int | None=None):
        self.id_pasajero = id_pasajero
        self.id_vuelo = id_vuelo
        self.num_reserva = num_reserva
        self.id = id
        self.fecha_venta = fecha_venta
        self.precio_pagado_usd = precio_pagado_usd
        self.id_estado_actual = id_estado_actual

    def to_dict(self):
        datos = {
            "id_pasajero": self.id_pasajero,
            "id_vuelo": self.id_vuelo,
            "num_reserva": self.num_reserva,
            "id": self.id,
            "fecha_venta": self.fecha_venta,
            "precio_pagado_usd": self.precio_pagado_usd,
            "id_estado_actual": self.id_estado_actual
        }

        return datos

class VentasManager(TablaManager):

    def __init__(self, db_manager):
        super().__init__("ventas", db_manager)
    
    def registrar_venta(self, id_staff: int, venta: Venta) -> None:
        if not self._verificar_campos_requeridos(venta):
            raise Exception("Error: no se ingresaron todos los campos requeridos.")
        
        if not self._verificar_pasajero(venta.id_pasajero):
            raise Exception("Error: el pasajero no se encuentra registrado.")
        
        if not self._verificar_capacidad(venta.id_vuelo):
            raise Exception("Error: no hay más asientos disponibles.")
        
        venta.num_reserva = self._generar_num_reserva()
        venta.id = None
        venta.fecha_venta = None
        venta.precio_pagado_usd = self._obtener_precio_pagado_usd(venta.id_vuelo)
        venta.id_estado_actual = 3


    def _verificar_campos_requeridos(self, venta: Venta) -> bool:
        campos_requeridos = ["id_pasajero", "id_vuelo"]

        for campo in campos_requeridos:
            if getattr(venta, campo) == None:
                return False
        
        return True
    
    def _obtener_precio_pagado_usd(self, id_vuelo: int) -> float:
        query = "SELECT precio_venta_usd FROM vuelos WHERE id = %s"

        consulta: list[tuple] = self.db_manager.consultar(query, (id_vuelo,))[0][0]

        if consulta:
            precio_venta_usd: float = consulta[0][0]
        else:
            raise Exception("Error: no se encontró ningún resultado al consultar.")

        return precio_venta_usd
    
    def _generar_num_reserva(self, longitud=6) -> str:
        caracteres = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
        num_reserva: str = ''.join(random.choice(caracteres) for _ in range(longitud))
        
        return num_reserva
    
    def _obtener_venta(self, id_venta: int) -> Venta:
        query = """
                SELECT  id_pasajero,
                        id_vuelo,
                        id,
                        num_reserva,
                        fecha_venta,
                        precio_pagado_usd,
                        id_estado_actual
                FROM    ventas
                WHERE   id = %s
                """
        
        consulta_venta: FilaVenta = self.db_manager.consultar(query, (id_venta,))[0]
        venta = Venta(*consulta_venta)

        return venta

    def _verificar_pasajero(self, id_pasajero: int) -> bool:
        query = "SELECT 1 FROM pasajeros where id = %s LIMIT 1"
        consulta: list[tuple] = self.db_manager.consultar(query, (id_pasajero,))

        if consulta:
            return True
        
        return False
    
    def _verificar_capacidad(self, id_vuelo: int) -> bool:
        num_ventas: int = self._obtener_num_ventas(id_vuelo)
        capacidad: int = self._obtener_capacidad(id_vuelo)

        if capacidad > num_ventas:
            return True
        
        return False
        
    def _obtener_capacidad(self, id_vuelo: int) -> int:
        query = """
                SELECT  a.capacidad
                FROM    ventas ve
                JOIN    vuelos vu
                ON      ve.id_vuelo = vu.id
                JOIN    aviones a
                ON      vu.id_avion = a.id
                WHERE   ve.id_vuelo = %s
                """

        consulta: list[tuple] = self.db_manager.consultar(query, (id_vuelo,))

        if consulta:
            capacidad: int = consulta[0][0]
        else:
            raise Exception("Error: el avión seleccionado no existe.")
        
        return capacidad
    
    def _obtener_num_ventas(self, id_vuelo: int) -> int:
        query = """
                SELECT      COUNT(id_vuelo) AS num_ventas
                FROM        ventas
                GROUP BY    id_vuelo
                WHERE       id = %s
                """

        consulta: list[tuple] = self.db_manager.consultar(query, (id_vuelo,))

        if consulta:
            num_ventas: int = consulta[0][0]
        else:
            raise Exception("Error: el vuelo selecionado no existe.")

        return num_ventas