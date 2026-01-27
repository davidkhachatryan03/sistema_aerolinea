from typing import Any

class AsignacionVueloBase:

    def __init__(self, fecha_inicio: int, fecha_fin: int, id_rol: int, id_vuelo: int, id_staff: int) -> None:
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

    def __init__(self, id: int, fecha_inicio: int, fecha_fin: int, id_rol: int, id_vuelo: int, id_staff: int) -> None:
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