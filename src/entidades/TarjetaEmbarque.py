from typing import Any
from datetime import datetime
from src.errores import ERROR_FORMATO_DATOS

class TarjetaEmbarqueBase:

    def __init__(self, id_estado_actual: int, id_venta: int) -> None:
        self.id_estado_actual = id_estado_actual
        self.id_venta = id_venta

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id_estado_actual": self.id_estado_actual,
            "id_venta": self.id_venta
        }

        return datos
    
    @property
    def id_estado_actual(self) -> int:
        return self._id_estado_actual
    
    @id_estado_actual.setter
    def id_estado_actual(self, valor: int) -> None:
        if not self._verificar_formato_id(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._id_estado_actual = valor

    @property
    def id_venta(self) -> int:
        return self._id_venta
    
    @id_venta.setter
    def id_venta(self, valor: int) -> None:
        if not self._verificar_formato_id(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._id_venta = valor
    
    def _verificar_formato_id(self, id: int) -> bool:
        if type(id) != int:
            return False
        
        if id <= 0:
            return False

        return True

class TarjetaEmbarqueDesdeDB(TarjetaEmbarqueBase):

    def __init__(self, id: int, fecha_emision: datetime, fecha_embarque: datetime | None, id_estado_actual: int, id_venta: int) -> None:
        super().__init__(id_estado_actual, id_venta)
        self.id = id
        self.fecha_emision = fecha_emision
        self.fecha_embarque = fecha_embarque

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id": self.id,
            "fecha_emision": self.fecha_emision,
            "fecha_embarque": self.fecha_embarque,
            "id_estado_actual": self.id_estado_actual,
            "id_venta": self.id_venta
        }

        return datos