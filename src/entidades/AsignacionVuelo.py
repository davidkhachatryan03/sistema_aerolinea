from typing import Any
from src.errores import ERROR_FORMATO_DATOS
from datetime import datetime

class AsignacionVueloBase:

    def __init__(self, fecha_inicio: datetime, fecha_fin: datetime, id_rol: int, id_vuelo: int, id_staff: int) -> None:
        if not self._verificar_fechas(fecha_inicio, fecha_fin) or not self._verificar_formato_id(id_rol) or not self._verificar_formato_id(id_vuelo) or not self._verificar_formato_id(id_staff):
            raise Exception(ERROR_FORMATO_DATOS)

        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.id_rol = id_rol
        self.id_vuelo = id_vuelo
        self.id_staff = id_staff

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "id_rol": self.id_rol,
            "id_vuelo": self.id_vuelo,
            "id_staff": self.id_staff
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

class AsignacionVueloDesdeDB(AsignacionVueloBase):

    def __init__(self, id: int, fecha_inicio: datetime, fecha_fin: datetime, id_rol: int, id_vuelo: int, id_staff: int) -> None:
        super().__init__(fecha_inicio, fecha_fin, id_rol, id_vuelo, id_staff)
        self.id = id

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id": self.id,
            "fecha_inicio": self.fecha_inicio,
            "fecha_fin": self.fecha_fin,
            "id_rol": self.id_rol,
            "id_vuelo": self.id_vuelo,
            "id_staff": self.id_staff
        }

        return datos