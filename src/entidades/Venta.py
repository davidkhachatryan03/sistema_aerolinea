from typing import Any
from datetime import datetime
from decimal import Decimal
from src.errores import ERROR_FORMATO_DATOS
import re

class VentaBase:

    def __init__(self, id_pasajero: int, id_vuelo: int, num_reserva: str, precio_pagado_usd: Decimal, id_estado_actual: int) -> None:
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
    
    @property
    def id_pasajero(self) -> int:
        return self._id_pasajero
    
    @id_pasajero.setter
    def id_pasajero(self, valor: int) -> None:
        if not self._verificar_formato_id(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._id_pasajero = valor

    @property
    def id_vuelo(self) -> int:
        return self._id_vuelo
    
    @id_vuelo.setter
    def id_vuelo(self, valor: int) -> None:
        if not self._verificar_formato_id(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._id_vuelo = valor

    @property
    def num_reserva(self) -> str:
        return self._num_reserva

    @num_reserva.setter
    def num_reserva(self, valor: str) -> None:
        if not self._verificar_formato_num_reserva(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._num_reserva = valor

    @property
    def precio_pagado_usd(self) -> Decimal:
        return self._precio_pagado_usd
    
    @precio_pagado_usd.setter
    def precio_pagado_usd(self, valor: Decimal) -> None:
        if not self._verificar_formato_precio_pagado_usd(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._precio_pagado_usd = valor

    @property
    def id_estado_actual(self) -> int:
        return self._id_estado_actual
    
    @id_estado_actual.setter
    def id_estado_actual(self, valor: int) -> None:
        if not self._verificar_formato_id(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._id_estado_actual = valor
    
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