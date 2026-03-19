from typing import Any
from src.errores import ERROR_FORMATO_DATOS
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
    
    @property
    def id_staff(self) -> int:
        return self._id_staff
    
    @id_staff.setter
    def id_staff(self, valor: int) -> None:
        if not self._verificar_formato_id(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._id_staff = valor

    @property
    def descripcion(self) -> str:
        return self._descripcion
    
    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        if type(valor) != str:
            raise Exception(ERROR_FORMATO_DATOS)
        self._descripcion = valor

    @property
    def licencia_hasta(self) -> datetime:
        return self._licencia_hasta
    
    @licencia_hasta.setter
    def licencia_hasta(self, valor: datetime) -> None:
        if type(valor) != datetime:
            raise Exception(ERROR_FORMATO_DATOS)
        self._licencia_hasta = valor
    
    def _verificar_formato_id(self, id: int) -> bool:
        if type(id) != int:
            return False
        
        if id <= 0:
            return False

        return True
    
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