from datetime import datetime
from typing import Any

class VueloBase:
    
    def __init__(self, id_ruta: int, id_avion: int, id_estado_actual: int, fecha_partida_programada: datetime, fecha_arribo_programada: datetime, costo_operativo_usd: float, precio_venta_usd: float) -> None:
        self.id_ruta = id_ruta
        self.id_avion = id_avion
        self.id_estado_actual = id_estado_actual
        self.fecha_partida_programada = fecha_partida_programada
        self.fecha_arribo_programada = fecha_arribo_programada
        self.costo_operativo_usd = costo_operativo_usd
        self.precio_venta_usd = precio_venta_usd

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id_ruta": self.id_ruta,
            "id_avion": self.id_avion,
            "id_estado_actual": self.id_estado_actual,
            "fecha_partida_programada": self.fecha_partida_programada,
            "fecha_arribo_programada": self.fecha_arribo_programada,
            "costo_operativo_usd": self.costo_operativo_usd,
            "precio_venta_usd": self.precio_venta_usd
        }

        return datos
    
class VueloDesdeDB(VueloBase):

    def __init__(self, id: int, id_ruta: int, id_avion: int, id_estado_actual: int, fecha_partida_programada: datetime, fecha_arribo_programada: datetime, costo_operativo_usd: float, precio_venta_usd: float, fecha_partida_real: datetime | None, fecha_arribo_real: datetime | None) -> None:
        super().__init__(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)
        self.id = id

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id": self.id,
            "fecha_partida_programada": self.fecha_partida_programada,
            "fecha_arribo_programada": self.fecha_arribo_programada,
            "fecha_partida_real": self.fecha_partida_programada,
            "fecha_arribo_real": self.fecha_arribo_programada,
            "costo_operativo_usd": self.costo_operativo_usd,
            "precio_venta_usd": self.precio_venta_usd,
            "id_ruta": self.id_ruta,
            "id_avion": self.id_avion,
            "id_estado_actual": self.id_estado_actual
        }

        return datos