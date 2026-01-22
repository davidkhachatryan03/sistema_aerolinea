from datetime import datetime
from typing import Any

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