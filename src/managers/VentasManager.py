from typing import Any
from datetime import datetime
from decimal import Decimal
import random
from src.tipos import FilaVenta
from src.managers.TablaManager import TablaManager
from src.entidades import VentaBase, VentaDesdeDB
from src.querys import OBTENER_VENTA, OBTENER_CAPACIDAD, OBTENER_NUM_VENTAS

class VentasManager(TablaManager):

    def __init__(self, db_manager):
        super().__init__("ventas", db_manager)
        self.estados_posibles = {
            1: "Pagado",
            2: "Reembolsado",
            3: "Reservado",
            4: "Fraude detectado"
        }
    
    def registrar_venta(self, id_staff: int, venta: VentaBase) -> None:
        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
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
    
    def _obtener_precio_pagado_usd(self, id_vuelo: int) -> Decimal:
        query = "SELECT precio_venta_usd FROM vuelos WHERE id = %s"

        consulta: list[tuple] = self.db_manager.consultar(query, (id_vuelo,))

        if consulta:
            precio_venta_usd: Decimal = consulta[0][0]
        else:
            raise Exception("Error: no se encontró ningún resultado al consultar.")

        return precio_venta_usd
    
    def _generar_num_reserva(self) -> str:
        num_reserva: str = ""

        letras = "ABCDEFGHIJK"
        numeros = "23456789"

        for _ in range(3):
            num_reserva += random.choice(letras)

        for _ in range(3):
            num_reserva += random.choice(numeros)

        return num_reserva
    
    def _obtener_venta(self, id_venta: int) -> VentaDesdeDB:
        query = OBTENER_VENTA
        
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

        if num_ventas == 0:
            return True

        capacidad: int = self._obtener_capacidad(id_vuelo)

        if capacidad > num_ventas:
            return True
        
        return False
        
    def _obtener_capacidad(self, id_vuelo: int) -> int:
        query = OBTENER_CAPACIDAD

        consulta: list[tuple] = self.db_manager.consultar(query, (id_vuelo,))

        if consulta:
            capacidad: int = consulta[0][0]
        else:
            raise Exception("Error: el avión seleccionado no existe.")
        
        return capacidad
    
    def _obtener_num_ventas(self, id_vuelo: int) -> int:
        query = OBTENER_NUM_VENTAS

        consulta: list[tuple] = self.db_manager.consultar(query, (id_vuelo,))

        if consulta:
            num_ventas: int = consulta[0][0]
        else:
            num_ventas = 0

        return num_ventas