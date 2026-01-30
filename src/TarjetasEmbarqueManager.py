from src.entidades.TarjetaEmbarque import TarjetaEmbarqueBase, TarjetaEmbarqueDesdeDB
from src.TablaManager import TablaManager
from datetime import datetime
from typing import Any

FilaTarjetaEmbarque = tuple[int, datetime, datetime | None, int, int]

class TarjetasEmbarqueManager(TablaManager):

    def __init__(self, db_manager):
        super().__init__("tarjetas_embarque", db_manager)
        self.estados_posibles = {
            1: "Emitida",
            2: "No Show",
            3: "Denegada",
            4: "Pendiente"
        }
        self.campos_requeridos = ["id_venta"]

    def registrar_tarjeta_embarque(self, id_staff: int, tarjeta_embarque: TarjetaEmbarqueBase) -> None:
        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        if not self._verificar_campos_requeridos(tarjeta_embarque):
            raise Exception("Error: no se ingresaron todos los campos requeridos.")

        datos: dict[str, Any] = tarjeta_embarque.to_dict() 

        super().agregar_fila(id_staff, datos)
    
    def registrar_fecha_embarque(self, id_tarjeta_embarque: int, id_staff: int, fecha_emision: datetime) -> None:
        if not super()._verificar_id_a_modificar(id_tarjeta_embarque):
            raise Exception("Error: el id a modificar no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        super().modificar_fila(id_tarjeta_embarque, id_staff, fecha_emision=fecha_emision)
    
    def cambiar_estado(self, id_tarjeta_embarque: int, id_staff: int, id_estado_actual: int) -> None:
        tarjeta_embarque: TarjetaEmbarqueDesdeDB = self._obtener_tarjeta_embarque(id_tarjeta_embarque)

        if not super()._verificar_id_a_modificar(id_tarjeta_embarque):
            raise Exception("Error: el id a modificar no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        if tarjeta_embarque.id_estado_actual == id_estado_actual:
            return
        
        super().modificar_fila(id_tarjeta_embarque, id_staff, id_estado_actual=id_estado_actual)
        
    def _verificar_campos_requeridos(self, tarjeta_embarque: TarjetaEmbarqueBase) -> bool:
        for campo in self.campos_requeridos:
            if getattr(tarjeta_embarque, campo) == None:
                return False
        
        return True
    
    def _obtener_tarjeta_embarque(self, id_tarjeta_embarque: int) -> TarjetaEmbarqueDesdeDB:
        query = """
                SELECT  id,
                        fecha_emision,
                        fecha_embarque,
                        id_estado_actual,
                        id_venta
                FROM    ventas
                WHERE   id = %s
                """
        
        consulta_tarjeta_embarque: list[tuple] = self.db_manager.consultar(query, (id_tarjeta_embarque,))

        if consulta_tarjeta_embarque:
            fila_tarjeta_embarque: FilaTarjetaEmbarque = consulta_tarjeta_embarque[0]
            tarjeta_embarque = TarjetaEmbarqueDesdeDB(*fila_tarjeta_embarque)
        else:
            raise Exception("Error: no existe tarjeta de embarque con el id ingresado.")
    
        return tarjeta_embarque