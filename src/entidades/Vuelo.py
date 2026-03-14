from typing import Any
from datetime import datetime
from decimal import Decimal
from src.errores import ERROR_FORMATO_DATOS

class VueloBase:
    
    def __init__(self, id_ruta: int, id_avion: int, id_estado_actual: int, fecha_partida_programada: datetime, fecha_arribo_programada: datetime, costo_operativo_usd: Decimal, precio_venta_usd: Decimal) -> None:
        if not self._verificar_formato_id(id_ruta) or not self._verificar_formato_id(id_avion) or not self._verificar_formato_id(id_estado_actual) or not self._verificar_fechas(fecha_partida_programada, fecha_arribo_programada) or not self._verificar_costo_operativo_usd(costo_operativo_usd) or not self._verificar_precio_venta_usd(precio_venta_usd):
            raise Exception(ERROR_FORMATO_DATOS)

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
    
    def _verificar_formato_id(self, id: int) -> bool:
        if type(id) != int:
            return False
        
        if id <= 0:
            return False

        return True
    
    def _verificar_fechas(self, fecha_partida_programada: datetime, fecha_arribo_programada: datetime) -> bool:
        if type(fecha_partida_programada) != datetime:
            return False
        
        if type(fecha_arribo_programada) != datetime:
            return False
        
        if fecha_partida_programada >= fecha_arribo_programada:
            return False
        
        return True
    
    def _verificar_costo_operativo_usd(self, costo_operativo_usd: Decimal) -> bool:
        if type(costo_operativo_usd) != Decimal:
            return False
        
        if costo_operativo_usd <= 0:
            return False
        
        return True
    
    def _verificar_precio_venta_usd(self, precio_venta_usd: Decimal) -> bool:
        if type(precio_venta_usd) != Decimal:
            return False
        
        if precio_venta_usd < 0:
            return False
        
        return True
    
class VueloDesdeDB(VueloBase):

    def __init__(self, id: int, fecha_partida_programada: datetime, fecha_arribo_programada: datetime, fecha_partida_real: datetime | None, fecha_arribo_real: datetime | None, costo_operativo_usd: Decimal, precio_venta_usd: Decimal, id_ruta: int, id_avion: int, id_estado_actual: int) -> None:
        super().__init__(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)
        self.id = id
        self.fecha_partida_real = fecha_partida_real
        self.fecha_arribo_real = fecha_arribo_real

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id": self.id,
            "fecha_partida_programada": self.fecha_partida_programada,
            "fecha_arribo_programada": self.fecha_arribo_programada,
            "fecha_partida_real": self.fecha_partida_real,
            "fecha_arribo_real": self.fecha_arribo_real,
            "costo_operativo_usd": self.costo_operativo_usd,
            "precio_venta_usd": self.precio_venta_usd,
            "id_ruta": self.id_ruta,
            "id_avion": self.id_avion,
            "id_estado_actual": self.id_estado_actual
        }

        return datos