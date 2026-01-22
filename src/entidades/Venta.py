from datetime import datetime
from typing import Any

class Venta:

    def __init__(self, id_pasajero: int, id_vuelo: int, num_reserva: str | None=None, fecha_venta: datetime | None=None, precio_pagado_usd: float | None=None, id_estado_actual: int | None=None, id: int | None=None,):
        self.id_pasajero = id_pasajero
        self.id_vuelo = id_vuelo
        self.num_reserva = num_reserva
        self.fecha_venta = fecha_venta
        self.precio_pagado_usd = precio_pagado_usd
        self.id_estado_actual = id_estado_actual
        self.id = id

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id_pasajero": self.id_pasajero,
            "id_vuelo": self.id_vuelo,
            "num_reserva": self.num_reserva,
            "fecha_venta": self.fecha_venta,
            "precio_pagado_usd": self.precio_pagado_usd,
            "id_estado_actual": self.id_estado_actual,
            "id": self.id,
        }

        return datos