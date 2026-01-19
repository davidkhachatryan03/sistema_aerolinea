from datetime import datetime
from typing import Any

class TarjetaEmbarque:

    def __init__(self, id_venta: int, id: int | None=None, fecha_emision: datetime | None=None, fecha_embarque: int | None=None, id_estado_actual: int | None=None) -> None:
        self.id_venta = id_venta
        self.id = id
        self.fecha_emision = fecha_emision
        self.fecha_embarque = fecha_embarque
        self.id_estado_actual = id_estado_actual

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id_venta": self.id_venta,
            "id": self.id,
            "fecha_emision": self.fecha_emision,
            "fecha_embarque": self.fecha_embarque,
            "id_estado_actual": self.id_estado_actual
        }

        return datos