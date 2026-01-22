from datetime import datetime
from typing import Any

class VentaBase:

    def __init__(self, id_pasajero: int, id_vuelo: int, num_reserva: str, precio_pagado_usd: float, id_estado_actual: int) -> None:
        self.id_pasajero = id_pasajero
        self.id_vuelo = id_vuelo
        self.num_reserva = num_reserva
        self.precio_pagado_usd = precio_pagado_usd
        self.id_estado_actual = id_estado_actual
    
    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id_pasajero": self.id_pasajero,
            "id_vuelo": self.id_vuelo,
            "num_reserva": self.num_reserva,
            "precio_pagado_usd": self.precio_pagado_usd,
            "id_estado_actual": self.id_estado_actual
        }

        return datos

class VentaDesdeDB(VentaBase):

    def __init__(self, fecha_venta: datetime, id: int, id_pasajero: int, id_vuelo: int, num_reserva: str, precio_pagado_usd: float, id_estado_actual: int) -> None:
        super().__init__(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)
        self.fecha_venta = fecha_venta
        self.id = id

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id": self.id,
            "num_reserva": self.num_reserva,
            "fecha_venta": self.fecha_venta,
            "precio_pagado_usd": self.precio_pagado_usd,
            "id_vuelo": self.id_vuelo,
            "id_estado_actual": self.id_estado_actual,
            "id_pasajero": self.id_pasajero
        }

        return datos