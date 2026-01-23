from datetime import datetime, date
from typing import Any

class DocumentoBase:

    def __init__(self, num_documento: str, fecha_vencimiento: date, pais_emision: str, id_pasajero: int, id_tipo_documento: int) -> None:
        self.num_documento = num_documento
        self.fecha_vencimiento = fecha_vencimiento
        self.pais_emision = pais_emision
        self.id_pasajero = id_pasajero
        self.id_tipo_documento = id_tipo_documento

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "num_documento": self.num_documento,
            "fecha_vencimiento": self.fecha_vencimiento,
            "pais_emision": self.pais_emision,
            "id_pasajero": self.id_pasajero,
            "id_tipo_documento": self.id_tipo_documento
        }

        return datos

class DocumentoDesdeDB(DocumentoBase):

    def __init__(self, id: int, num_documento: str, fecha_vencimiento: datetime, pais_emision: str, id_pasajero: int, id_tipo_documento: int) -> None:
        super().__init__(num_documento, fecha_vencimiento, pais_emision, id_pasajero, id_tipo_documento)
        self.id = id

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id": self.id,
            "num_documento": self.num_documento,
            "fecha_vencimiento": self.fecha_vencimiento,
            "pais_emision": self.pais_emision,
            "id_pasajero": self.id_pasajero,
            "id_tipo_documento": self.id_tipo_documento
        }

        return datos