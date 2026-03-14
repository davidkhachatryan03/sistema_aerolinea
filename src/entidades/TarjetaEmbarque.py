from typing import Any
from datetime import datetime
from src.errores import ERROR_FORMATO_DATOS

class TarjetaEmbarqueBase:

    def __init__(self, id_estado_actual: int, id_venta: int) -> None:
        if type(id_estado_actual) != int or type(id_venta) != int:
            raise Exception(ERROR_FORMATO_DATOS)

        self.id_estado_actual = id_estado_actual
        self.id_venta = id_venta

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id_estado_actual": self.id_estado_actual,
            "id_venta": self.id_venta
        }

        return datos

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