from typing import Any
from datetime import datetime

class CertificacionStaffBase:

    def __init__(self, id_staff: int, descripcion: str, licencia_hasta: datetime) -> None:
        self.id_staff = id_staff
        self.descripcion = descripcion
        self.licencia_hasta = licencia_hasta

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id_staff": self.id_staff,
            "descripcion": self.descripcion,
            "licencia_hasta": self.licencia_hasta
        }

        return datos
    
class CertificacionStaffDesdeDB(CertificacionStaffBase):

    def __init__(self, id: int, id_staff: int, descripcion: str, licencia_hasta: datetime) -> None:
        super().__init__(id_staff, descripcion, licencia_hasta)
        self.id = id

    def to_dict(self) -> dict[str, Any]:
        datos = {
            "id": self.id,
            "id_staff": self.id_staff,
            "descripcion": self.descripcion,
            "licencia_hasta": self.licencia_hasta
        }

        return datos