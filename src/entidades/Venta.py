from typing import Any
from datetime import datetime
from decimal import Decimal
import re

class VentaBase:

    def __init__(self, id_pasajero: int, id_vuelo: int, num_reserva: str, precio_pagado_usd: Decimal, id_estado_actual: int) -> None:
        if not self._verificar_formato_id(id_pasajero) or not self._verificar_formato_id(id_vuelo) or not self._verificar_formato_id(id_estado_actual) or not self._verificar_formato_num_reserva(num_reserva) or not self._verificar_formato_precio_pagado_usd(precio_pagado_usd):
            raise Exception("Error: el formato de los datos es incorrecto.")

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
    
    def _verificar_formato_id(self, id: int) -> bool:
        if type(id) != int:
            return False
        
        if id <= 0:
            return False

        return True
    
    def _verificar_formato_num_reserva(self, num_reserva: str) -> bool:
        patron_num_reserva = r"^[A-K]{3}\d{3}$"

        if type(num_reserva) != str:
            return False
        
        if len(num_reserva) != 6:
            return False
        
        if not re.match(patron_num_reserva, num_reserva):
            return False
        
        return True
    
    def _verificar_formato_precio_pagado_usd(self, precio_pagado_usd: Decimal) -> bool:
        if type(precio_pagado_usd) != Decimal:
            return False
        
        if precio_pagado_usd < 0:
            return False
        
        return True

class VentaDesdeDB(VentaBase):

    def __init__(self, id: int, num_reserva: str, fecha_venta: datetime, precio_pagado_usd: Decimal, id_vuelo: int, id_estado_actual: int, id_pasajero: int) -> None:
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