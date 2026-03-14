from typing import Any
from decimal import Decimal
from src.errores import ERROR_FORMATO_DATOS

class AvionBase:

    def __init__(self, matricula: str, marca: str, modelo: str, capacidad: int, autonomia_km: int, costo_hora_vuelo: Decimal, id_estado_actual: int) -> None:
        if type(matricula) != str or type(marca) != str or type(modelo) != str or not self._verificar_formato_capacidad(capacidad) or not self._verificar_formato_autonomia_km(autonomia_km) or not self._verificar_costo_hora_vuelo(costo_hora_vuelo) or not self._verificar_formato_id(id_estado_actual):
            raise Exception(ERROR_FORMATO_DATOS)

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
    
    def _verificar_formato_id(self, id: int) -> bool:
        if type(id) != int:
            return False
        
        if id <= 0:
            return False

        return True
    
    def _verificar_formato_capacidad(self, capacidad: int) -> bool:
        if type(capacidad) != int:
            return False
        
        if capacidad <= 0:
            return False
        
        return True
    
    def _verificar_formato_autonomia_km(self, autonomia_km: int) -> bool:
        if type(autonomia_km) != int:
            return False
        
        if autonomia_km <= 0:
            return False
        
        return True
    
    def _verificar_costo_hora_vuelo(self, costo_hora_vuelo: Decimal) -> bool:
        if type(costo_hora_vuelo) != Decimal:
            return False
        
        if costo_hora_vuelo <= 0:
            return False
        
        return True

class AvionDesdeDB(AvionBase):

    def __init__(self, id: int, matricula: str, marca: str, modelo: str, capacidad: int, autonomia_km: int, costo_hora_vuelo: Decimal, id_estado_actual: int) -> None:
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