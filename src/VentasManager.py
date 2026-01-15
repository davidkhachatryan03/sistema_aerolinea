from TablaManager import TablaManager
from datetime import datetime
from typing import Any
from collections.abc import Iterable
import random

FilaVenta = tuple[int, int, str | None, datetime | None, float | None, int | None]

class Venta:

    def __init__(self, id_pasajero: int, id_vuelo: int, num_reserva: str | None=None, fecha_venta: datetime | None=None, precio_pagado_usd: float | None=None, id_estado_actual: int | None=None):
        self.id_pasajero = id_pasajero
        self.id_vuelo = id_vuelo
        self.num_reserva = num_reserva
        self.fecha_venta = fecha_venta
        self.precio_pagado_usd = precio_pagado_usd
        self.id_estado_actual = id_estado_actual

    def to_dict(self):
        datos = {
            "id_pasajero": self.id_pasajero,
            "id_vuelo": self.id_vuelo,
            "num_reserva": self.num_reserva,
            "fecha_venta": self.fecha_venta,
            "precio_pagado_usd": self.precio_pagado_usd,
            "id_estado_actual": self.id_estado_actual
        }

        return datos

class VentasManager(TablaManager):

    def __init__(self, db_manager):
        super().__init__("ventas", db_manager)
    
    def agregar_fila(self, id_staff, venta: Venta) -> None:
        if not self._verificar_campos_requeridos(venta):
            raise Exception("Error: no se ingresaron todos los campos requeridos.")
        
        venta.precio_pagado_usd = self._obtener_precio_pagado_usd(venta.id_vuelo)
        
        venta.id_estado_actual = 1

        venta.num_reserva = self._generar_num_reserva()
        
        datos: dict[str, Any] = venta.to_dict()

        super().agregar_fila(id_staff, datos)

    def modificar_fila(self, id_venta: int, id_staff: int, **datos_nuevos):
        consulta_venta: FilaVenta = self._obtener_venta(id_venta)
        venta = Venta(*consulta_venta)

        campos_posibles: Iterable[str] = venta.to_dict().keys()

        nuevos_valores = []

        for campo in campos_posibles:
            if campo in datos_nuevos:
                nuevos_valores.append(datos_nuevos[campo])
            else:
                nuevos_valores.append(getattr(venta, campo))

        vuelo_modificado = Venta(*nuevos_valores)

        

    def _verificar_campos_requeridos(self, venta: Venta) -> bool:
        campos_requeridos = ["id_pasajero", "id_vuelo"]

        for campo in campos_requeridos:
            if getattr(venta, campo) == None:
                return False
        
        return True
    
    def _obtener_precio_pagado_usd(self, id_vuelo: int) -> float:
        query = "SELECT precio_venta_usd FROM vuelos WHERE id = %s"

        precio_venta_usd: float = self.db_manager.consultar(query, (id_vuelo,))[0][0]

        return precio_venta_usd
    
    def _generar_num_reserva(self, longitud=6) -> str:
        caracteres = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"
        num_reserva: str = ''.join(random.choice(caracteres) for _ in range(longitud))
        
        return num_reserva
    
    def _obtener_venta(self, id_venta: int) -> FilaVenta:
        query = """
                SELECT  id_pasajero,
                        id_vuelo,
                        num_reserva,
                        fecha_venta,
                        precio_pagado_usd,
                        id_estado_actual
                FROM    ventas
                WHERE   id = %s
                """
        
        venta: FilaVenta = self.db_manager.consultar(query, (id_venta,))[0]

        return venta