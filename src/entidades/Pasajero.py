from typing import Any

class Pasajero:

    def __init__(self, nombre_completo: str, email: str, telefono: int, esta_en_lista_negra: bool, es_vip: bool, id: int | None=None) -> None:
        self.nombre_completo = nombre_completo
        self.email = email
        self.telefono = telefono
        self.esta_en_lista_negra = esta_en_lista_negra
        self.es_vip = es_vip
        self.id = id

    def to_dict(self, incluir_id: bool=False) -> dict[str, Any]:
        datos = {
            "nombre_completo": self.nombre_completo,
            "email": self.email,
            "telefono": self.email,
            "esta_en_lista_negra": self.esta_en_lista_negra,
            "es_vip": self.es_vip,
        }

        if incluir_id and self.id is not None:
            datos["id"] = self.id

        return datos