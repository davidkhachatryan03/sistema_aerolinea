from src.entidades.TarjetaEmbarque import TarjetaEmbarque
from src.TablaManager import TablaManager
from typing import Any

class TarjetaEmbarqueManager(TablaManager):

    def __init__(self, db_manager):
        super().__init__("tarjetas_embarque", db_manager)
        self.estados_posibles = {
            1: "Emitida",
            2: "No Show",
            3: "Denegada",
            4: "Pendiente"
        }
        self.campos_requeridos = ["id_venta"]

    def registrar_tarjeta_embarque(self, id_staff: int, tarjeta_embarque: TarjetaEmbarque) -> None:
        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        if not self._verificar_campos_requeridos(tarjeta_embarque):
            raise Exception("Error: no se ingresaron todos los campos requeridos.")
        
        tarjeta_embarque.id_estado_actual = 4
        tarjeta_embarque.id = None
        tarjeta_embarque.fecha_emision = None
        tarjeta_embarque.fecha_embarque = None

        datos: dict[str, Any] = tarjeta_embarque.to_dict() 

        super().agregar_fila(id_staff, datos)
        
        
    def _verificar_campos_requeridos(self, tarjeta_embarque: TarjetaEmbarque) -> bool:
        for campo in self.campos_requeridos:
            if getattr(tarjeta_embarque, campo) == None:
                return False
        
        return True