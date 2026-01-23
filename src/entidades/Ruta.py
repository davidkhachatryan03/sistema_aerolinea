from typing import Any

class RutaBase:

    def __init__(self, num_vuelo: str, origen: str, destino: str, distancia_km: int, duracion_min: int) -> None:
        self.num_vuelo = num_vuelo
        self.origen = origen
        self.destino = destino
        self.distancia_km = distancia_km
        self.duracion_min = duracion_min

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "num_vuelo": self.num_vuelo,
            "origen": self.origen,
            "destino": self.destino,
            "distancia_km": self.distancia_km,
            "duracion_min": self.duracion_min
        }

        return datos
    

class RutaDesdeDB(RutaBase):

    def __init__(self, id: int, num_vuelo: str, origen: str, destino: str, distancia_km: int, duracion_min: int) -> None:
        super().__init__(num_vuelo, origen, destino, distancia_km, duracion_min)
        self.id = id

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id": self.id,
            "num_vuelo": self.num_vuelo,
            "origen": self.origen,
            "destino": self.destino,
            "distancia_km": self.distancia_km,
            "duracion_min": self.duracion_min
        }

        return datos