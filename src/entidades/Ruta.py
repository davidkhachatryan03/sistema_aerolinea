from typing import Any
from src.errores import ERROR_FORMATO_DATOS
import re 

class RutaBase:

    def __init__(self, num_vuelo: str, origen: str, destino: str, distancia_km: int, duracion_min: int) -> None:
        if not self._verificar_num_vuelo(num_vuelo) or type(origen) != str or type(destino) != str or not self._verificar_distancia_km(distancia_km) or not self._verificar_duracion_min(duracion_min):
            raise Exception(ERROR_FORMATO_DATOS)

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
    
    def _verificar_num_vuelo(self, num_vuelo: str) -> bool:
        patron_num_vuelo = r'^[A-Z]{2}\d{4}$'

        if type(num_vuelo) != str:
            return False
        
        if not re.match(patron_num_vuelo, num_vuelo):
            return False
        
        return True
    
    def _verificar_distancia_km(self, distancia_km: int) -> bool:
        if type(distancia_km) != int:
            return False
        
        if distancia_km <= 0:
            return False
        
        return True
    
    def _verificar_duracion_min(self, durancion_min: int) -> bool:
        if type(self.duracion_min != int):
            return False
        
        if self.duracion_min <= 0:
            return False
        
        return True

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