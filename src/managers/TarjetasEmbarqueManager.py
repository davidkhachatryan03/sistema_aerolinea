from typing import Any
from datetime import datetime
from src.tipos import FilaTarjetaEmbarque
from src.managers.TablaManager import TablaManager
from src.entidades import TarjetaEmbarqueBase, TarjetaEmbarqueDesdeDB
from src.querys import OBTENER_TARJETA_EMBARQUE
from src.errores import *

class TarjetasEmbarqueManager(TablaManager):

    def __init__(self, db_manager):
        super().__init__("tarjetas_embarque", db_manager)
        self.campos_requeridos = ["id_venta"]
        self.estados_posibles = {
            1: "Emitida",
            2: "No Show",
            3: "Denegada",
            4: "Pendiente"
        }

    def registrar_tarjeta_embarque(self, id_staff: int, tarjeta_embarque: TarjetaEmbarqueBase) -> None:
        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        # a futuro este método será eliminado
        if not self._verificar_campos_requeridos(tarjeta_embarque):
            raise Exception("Error: no se ingresaron todos los campos requeridos.")

        datos: dict[str, Any] = tarjeta_embarque.to_dict() 

        super().agregar_fila(id_staff, datos)
    
    def registrar_fecha_embarque(self, id_tarjeta_embarque: int, id_staff: int, fecha_emision: datetime) -> None:
        if not super()._verificar_id_a_modificar(id_tarjeta_embarque):
            raise Exception(ERROR_ID_INVALIDO)

        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        super().modificar_fila(id_tarjeta_embarque, id_staff, "fecha_emision", fecha_emision)
    
    def cambiar_estado(self, id_tarjeta_embarque: int, id_staff: int, id_estado_actual: int) -> None:
        tarjeta_embarque: TarjetaEmbarqueDesdeDB = self._obtener_tarjeta_embarque(id_tarjeta_embarque)

        if not super()._verificar_id_a_modificar(id_tarjeta_embarque):
            raise Exception(ERROR_ID_INVALIDO)

        if not super()._verificar_id_staff(id_staff):
            raise Exception(ERROR_STAFF_INVALIDO)
        
        if tarjeta_embarque.id_estado_actual == id_estado_actual:
            return
        
        super().modificar_fila(id_tarjeta_embarque, id_staff, "id_estado_actual", id_estado_actual)
        
    def _verificar_campos_requeridos(self, tarjeta_embarque: TarjetaEmbarqueBase) -> bool:
        for campo in self.campos_requeridos:
            if getattr(tarjeta_embarque, campo) == None:
                return False
        
        return True
    
    def _obtener_tarjeta_embarque(self, id_tarjeta_embarque: int) -> TarjetaEmbarqueDesdeDB:
        query = OBTENER_TARJETA_EMBARQUE
        
        consulta_tarjeta_embarque: list[tuple] = self.db_manager.consultar(query, (id_tarjeta_embarque,))
        fila_tarjeta_embarque: FilaTarjetaEmbarque = consulta_tarjeta_embarque[0]
        tarjeta_embarque = TarjetaEmbarqueDesdeDB(*fila_tarjeta_embarque)

        return tarjeta_embarque