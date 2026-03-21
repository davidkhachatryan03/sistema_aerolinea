from typing import Any

class StaffBase:

    def __init__(self, nombre_completo: str, id_estado_actual: int, id_cargo_actual: int) -> None:
        self.nombre_completo = nombre_completo
        self.id_estado_actual = id_estado_actual
        self.id_cargo_actual = id_cargo_actual

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "nombre_completo": self.nombre_completo,
            "id_estado_actual": self.id_estado_actual,
            "id_cargo_actual": self.id_cargo_actual
        }

        return datos

class StaffDesdeDB(StaffBase):

    def __init__(self, id: int, nombre_completo: str, id_estado_actual: int, id_cargo_actual: int) -> None:
        self.id = id
        super().__init__(nombre_completo, id_estado_actual, id_cargo_actual)

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id": self.id,
            "nombre_completo": self.nombre_completo,
            "id_estado_actual": self.id_estado_actual,
            "id_cargo_actual": self.id_cargo_actual
        }

        return datos