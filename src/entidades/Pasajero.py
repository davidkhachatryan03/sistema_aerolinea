from typing import Any

class PasajeroBase:

    def __init__(self, nombre_completo: str, email: str, telefono: str, esta_en_lista_negra: bool, es_vip: bool) -> None:
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
    

class PasajeroDesdeDB(PasajeroBase):

    def __init__(self, id: int, nombre_completo: str, email: str, telefono: str, esta_en_lista_negra: bool, es_vip: bool) -> None:
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