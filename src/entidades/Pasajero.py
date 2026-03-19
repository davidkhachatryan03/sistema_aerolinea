from typing import Any
from src.errores import ERROR_FORMATO_DATOS

class PasajeroBase:

    def __init__(self, nombre_completo: str, email: str, telefono: int, esta_en_lista_negra: bool, es_vip: bool) -> None:
        self.nombre_completo = nombre_completo
        self.email = email
        self.telefono = telefono
        self.esta_en_lista_negra = esta_en_lista_negra
        self.es_vip = es_vip

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "nombre_completo": self.nombre_completo,
            "email": self.email,
            "telefono": self.telefono,
            "esta_en_lista_negra": self.esta_en_lista_negra,
            "es_vip": self.es_vip
        }

        return datos
    
    @property
    def nombre_completo(self) -> str:
        return self._nombre_completo
    
    @nombre_completo.setter
    def nombre_completo(self, valor: str) -> None:
        if type(valor) != str:
            raise Exception(ERROR_FORMATO_DATOS)
        self._nombre_completo = valor

    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, valor: str) -> None:
        if type(valor) != str:
            raise Exception(ERROR_FORMATO_DATOS)
        self._email = valor

    @property
    def telefono(self) -> int:
        return self._telefono
    
    @telefono.setter
    def telefono(self, valor: int) -> None:
        if type(valor) != int:
            raise Exception(ERROR_FORMATO_DATOS)
        self._telefono = valor

    @property
    def esta_en_lista_negra(self) -> bool:
        return self._esta_en_lista_negra
    
    @esta_en_lista_negra.setter
    def esta_en_lista_negra(self, valor: bool) -> None:
        if not self._verificar_booleano(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._esta_en_lista_negra = bool(valor)

    @property
    def es_vip(self) -> bool:
        return self._es_vip
    
    @es_vip.setter
    def es_vip(self, valor: bool) -> None:
        if not self._verificar_booleano(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._es_vip = bool(valor)
    
    def _verificar_booleano(self, valor: bool) -> bool:
        if type(valor) not in [bool, int]:
            return False
        
        if int(valor) not in [0, 1]:
            return False
        
        return True

class PasajeroDesdeDB(PasajeroBase):

    def __init__(self, id: int, nombre_completo: str, email: str, telefono: int, esta_en_lista_negra: bool, es_vip: bool) -> None:
        super().__init__(nombre_completo, email, telefono, esta_en_lista_negra, es_vip)
        self.id = id

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id": self.id,
            "nombre_completo": self.nombre_completo,
            "email": self.email,
            "telefono": self.telefono,
            "esta_en_lista_negra": self.esta_en_lista_negra,
            "es_vip": self.es_vip
        }

        return datos