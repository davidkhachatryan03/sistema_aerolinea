from typing import Any
from datetime import datetime

class AsignacionVueloBase:

    def __init__(self, fecha_inicio: datetime, fecha_fin: datetime, id_rol: int, id_vuelo: int, id_staff: int) -> None:
        if type(fecha_inicio) != datetime or type(fecha_fin) != datetime or type(id_rol) != int or type(id_vuelo) != int or type(id_staff) != int:
            raise Exception("Error: el formato de los datos es incorrecto.")

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