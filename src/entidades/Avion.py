from typing import Any
from decimal import Decimal
from src.errores import ERROR_FORMATO_DATOS

class AvionBase:

    def __init__(self, matricula: str, marca: str, modelo: str, capacidad: int, autonomia_km: int, costo_hora_vuelo: Decimal, id_estado_actual: int) -> None:
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
    
    @property
    def matricula(self) -> str:
        return self._matricula
    
    @matricula.setter
    def matricula(self, valor: str) -> None:
        if type(valor) != str:
            raise Exception(ERROR_FORMATO_DATOS)
        self._matricula = valor

    @property
    def marca(self) -> str:
        return self._marca
    
    @marca.setter
    def marca(self, valor: str) -> None:
        if type(valor) != str:
            raise Exception(ERROR_FORMATO_DATOS)
        self._marca = valor

    @property
    def modelo(self) -> str:
        return self._modelo
    
    @modelo.setter
    def modelo(self, valor: str) -> None:
        if type(valor) != str:
            raise Exception(ERROR_FORMATO_DATOS)
        self._modelo = valor

    @property
    def capacidad(self) -> int:
        return self._capacidad
    
    @capacidad.setter
    def capacidad(self, valor: int) -> None:
        if not self._verificar_formato_capacidad(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._capacidad = valor

    @property
    def autonomia_km(self) -> int:
        return self._autonomia_km
    
    @autonomia_km.setter
    def autonomia_km(self, valor: int) -> None:
        if not self._verificar_formato_autonomia_km(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._autonomia_km = valor

    @property
    def costo_hora_vuelo(self) -> Decimal:
        return self._costo_hora_vuelo
    
    @costo_hora_vuelo.setter
    def costo_hora_vuelo(self, valor: Decimal) -> None:
        if not self._verificar_costo_hora_vuelo(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._costo_hora_vuelo = valor

    @property
    def id_estado_actual(self) -> int:
        return self._id_estado_actual
    
    @id_estado_actual.setter
    def id_estado_actual(self, valor: int) -> None:
        if not self._verificar_formato_id(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._id_estado_actual = valor
    
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