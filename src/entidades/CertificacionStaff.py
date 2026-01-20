from typing import Any
from datetime import datetime

class CertificacionStaff:

    def __init__(self, id_staff: int, descripcion: str, licencia_hasta: datetime, id: int | None=None) -> None:
        self.id_staff = id_staff
        self.descripcion = descripcion
        self.licencia_hasta = licencia_hasta
        self.id = id

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id_staff": self.id_staff,
            "descripcion": self.descripcion,
            "licencia_hasta": self.licencia_hasta,
            "id": self.id
        }

        return datos
