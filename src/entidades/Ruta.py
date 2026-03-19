from typing import Any
from src.errores import ERROR_FORMATO_DATOS
import re 

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
    
    @property
    def num_vuelo(self) -> str:
        return self._num_vuelo
    
    @num_vuelo.setter
    def num_vuelo(self, valor: str) -> None:
        if not self._verificar_num_vuelo(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._num_vuelo = valor

    @property
    def origen(self) -> str:
        return self._origen
    
    @origen.setter
    def origen(self, valor: str) -> None:
        if not self._verificar_aeropuerto(valor):
            raise  Exception(ERROR_FORMATO_DATOS)
        self._origen = valor

    @property
    def destino(self) -> str:
        return self._destino
    
    @destino.setter
    def destino(self, valor: str) -> None:
        if not self._verificar_aeropuerto(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._destino = valor

    @property
    def distancia_km(self) -> int:
        return self._distancia_km
    
    @distancia_km.setter
    def distancia_km(self, valor: int) -> None:
        if not self._verificar_distancia_km(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._distancia_km = valor

    @property
    def duracion_min(self) -> int:
        return self._duracion_min
    
    @duracion_min.setter
    def duracion_min(self, valor: int) -> None:
        if not self._verificar_duracion_min(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._duracion_min = valor
    
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
    
    def _verificar_duracion_min(self, duracion_min: int) -> bool:
        if type(duracion_min) != int:
            return False
        
        if duracion_min <= 0:
            return False
        
        return True
    
    def _verificar_aeropuerto(self, valor: str) -> bool:
        if type(valor) != str:
            return False
        
        if len(valor) != 3:
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