from typing import Any

class AvionBase:

    def __init__(self, matricula: str, marca: str, modelo: str, capacidad: str, autonomia_km: str, costo_hora_vuelo: float, id_estado_actual: int) -> None:
        self.matricula = matricula
        self.marca = marca
        self.modelo = modelo
        self.capacidad = capacidad
        self.autonomia_km = autonomia_km
        self.costo_hora_vuelo = costo_hora_vuelo
        self.id_estado_actual = id_estado_actual

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "matricula": self.matricula,
            "marca": self.marca,
            "modelo": self.modelo,
            "capacidad": self.capacidad,
            "autonomia_km": self.autonomia_km,
            "costo_hora_vuelo": self.costo_hora_vuelo,
            "id_estado_actual": self.id_estado_actual
        }

        return datos
    

class AvionDesdeDB(AvionBase):

    def __init__(self, id: int, matricula: str, marca: str, modelo: str, capacidad: str, autonomia_km: str, costo_hora_vuelo: float, id_estado_actual: int) -> None:
        super().__init__(matricula, marca, modelo, capacidad, autonomia_km, costo_hora_vuelo, id_estado_actual)
        self.id = id

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id": self.id,
            "matricula": self.matricula,
            "marca": self.marca,
            "modelo": self.modelo,
            "capacidad": self.capacidad,
            "autonomia_km": self.autonomia_km,
            "costo_hora_vuelo": self.costo_hora_vuelo,
            "id_estado_actual": self.id_estado_actual
        }

        return datos