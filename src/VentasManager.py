from TablaManager import TablaManager
from datetime import datetime
from typing import Any
from collections.abc import Iterable
from src.entidades.Venta import VentaBase, VentaDesdeDB
import random

FilaVenta = tuple[datetime, int, int, int, str, float, int]

class VentasManager(TablaManager):

    def __init__(self, db_manager):
        super().__init__("ventas", db_manager)
        self.campos_requeridos = ["id_pasajero", "id_vuelo"]
        self.estados_posibles = {
            1: "Pagado",
            2: "Reembolsado",
            3: "Reservado",
            4: "Fraude detectado"
        }
    
    def registrar_venta(self, id_staff: int, venta: VentaBase) -> None:
        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        if not self._verificar_campos_requeridos(venta):
            raise Exception("Error: no se ingresaron todos los campos requeridos.")
        
        if not self._verificar_pasajero(venta.id_pasajero):
            raise Exception("Error: el pasajero no se encuentra registrado.")
        
        if not self._verificar_vuelo(venta.id_vuelo):
            raise Exception("Error: el vuelo no se encuentra registrado.")
        
        if not self._verificar_capacidad(venta.id_vuelo):
            raise Exception("Error: no hay más asientos disponibles.")
        
        venta.num_reserva = self._generar_num_reserva()
        venta.precio_pagado_usd = self._obtener_precio_pagado_usd(venta.id_vuelo)
        venta.id_estado_actual = 3

        datos: dict[str, Any] = venta.to_dict()

        super().agregar_fila(id_staff, datos)
    
    def modificar_num_reserva(self, id_staff: int, id_venta: int) -> None:
        if not super()._verificar_id_a_modificar(id_venta):
            raise Exception("Error: el id a modificar no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        num_reserva: str = self._generar_num_reserva()

        super().modificar_fila(id_venta, id_staff, num_reserva=num_reserva)

    def modificar_estado(self, id_venta: int, id_staff: int, id_estado_actual: int) -> None:
        venta: VentaDesdeDB = self._obtener_venta(id_venta)

        if not super()._verificar_id_a_modificar(id_venta):
            raise Exception("Error: el id a modificar no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        if id_estado_actual not in self.estados_posibles:
            raise Exception("Error: el estado ingresado no existe.")
        
        if venta.id_estado_actual == id_estado_actual:
            return
        
        super().modificar_fila(id_venta, id_staff, id_estado_actual=id_estado_actual)
    
    def cambiar_vuelo(self, id_venta: int, id_staff: int, id_vuelo: int) -> None:
        venta: VentaDesdeDB = self._obtener_venta(id_venta)

        if not super()._verificar_id_a_modificar(id_venta):
            raise Exception("Error: el id a modificar no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        if not self._verificar_vuelo(venta.id_vuelo):
            raise Exception("Error: el vuelo no se encuentra registrado.")
        
        if venta.id_vuelo == id_vuelo:
            return
        
        precio_pagado_usd = self._obtener_precio_pagado_usd(id_vuelo)
        
        super().modificar_fila(id_venta, id_staff, id_vuelo=id_vuelo, precio_pagado_usd = precio_pagado_usd)
    
    def cambiar_pasajero(self, id_venta: int, id_staff: int, id_pasajero: int) -> None:
        venta: VentaDesdeDB = self._obtener_venta(id_venta)
        
        if not super()._verificar_id_a_modificar(id_venta):
            raise Exception("Error: el id a modificar no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        if not self._verificar_pasajero(id_pasajero):
            raise Exception("Error: el pasajero ingresado no existe.")
        
        if venta.id_pasajero == id_pasajero:
            return

    def _verificar_campos_requeridos(self, venta: VentaBase) -> bool:
        for campo in self.campos_requeridos:
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
    
    def _obtener_venta(self, id_venta: int) -> VentaDesdeDB:
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
        
        consulta_venta: list[tuple] = self.db_manager.consultar(query, (id_venta,))

        if consulta_venta:
            fila_venta: FilaVenta = consulta_venta[0]
            venta = VentaDesdeDB(*fila_venta)

        return venta
    
    def _verificar_vuelo(self, id_vuelo: int):
        query = "SELECT 1 FROM pasajeros WHERE id = %s LIMIT 1"
        consulta: list[tuple] = self.db_manager.consultar(query, (id_vuelo,))

        if consulta:
            return True
        
        return False

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