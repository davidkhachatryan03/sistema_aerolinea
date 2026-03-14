from typing import Any
from src.errores import ERROR_FORMATO_DATOS

class PasajeroBase:

    def __init__(self, nombre_completo: str, email: str, telefono: int, esta_en_lista_negra: bool, es_vip: bool) -> None:
        if type(nombre_completo) != str or type(email) != str or type(telefono) != int or not self._verificar_booleanos(esta_en_lista_negra, es_vip):
            raise Exception(ERROR_FORMATO_DATOS)
        
        self.nombre_completo = nombre_completo
        self.email = email
        self.telefono = telefono
        self.esta_en_lista_negra = bool(esta_en_lista_negra)
        self.es_vip = bool(es_vip)

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "nombre_completo": self.nombre_completo,
            "email": self.email,
            "telefono": self.telefono,
            "esta_en_lista_negra": self.esta_en_lista_negra,
            "es_vip": self.es_vip
        }

        return datos
    
    def _verificar_booleanos(self, esta_en_lista_negra, es_vip) -> bool:
        if type(esta_en_lista_negra) not in [bool, int]:
            return False
        
        if type(es_vip) not in [bool, int]:
            return False
        
        if int(esta_en_lista_negra) not in [0, 1]:
            return False
        
        if int(es_vip) not in [0, 1]:
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