from typing import Any
from src.errores import ERROR_FORMATO_DATOS
from datetime import date

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
    
    @property
    def num_documento(self) -> str:
        return self._num_documento
    
    @num_documento.setter
    def num_documento(self, valor: str) -> None:
        if type(valor) != str:
            raise Exception(ERROR_FORMATO_DATOS)
        self._num_documento = valor

    @property
    def fecha_vencimiento(self) -> date:
        return self._fecha_vencimiento
    
    @fecha_vencimiento.setter
    def fecha_vencimiento(self, valor: date) -> None:
        if type(valor) != date:
            raise Exception(ERROR_FORMATO_DATOS)
        self._fecha_vencimiento = valor

    @property
    def pais_emision(self) -> str:
        return self._pais_emision
    
    @pais_emision.setter
    def pais_emision(self, valor: str) -> None:
        if type(valor) != str:
            raise Exception(ERROR_FORMATO_DATOS)
        self._pais_emision = valor

    @property
    def id_pasajero(self) -> int:
        return self._id_pasajero
    
    @id_pasajero.setter
    def id_pasajero(self, valor: int) -> None:
        if not self._verificar_formato_id(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._id_pasajero = valor

    @property
    def id_tipo_documento(self) -> int:
        return self._id_tipo_documento

    @id_tipo_documento.setter
    def id_tipo_documento(self, valor: int) -> None:
        if not self._verificar_formato_id(valor):
            raise Exception(ERROR_FORMATO_DATOS)
        self._id_tipo_documento = valor
    
    def _verificar_formato_id(self, id: int) -> bool:
        if type(id) != int:
            return False
        
        if id <= 0:
            return False

        return True

class DocumentoDesdeDB(DocumentoBase):

    def __init__(self, id: int, num_documento: str, fecha_vencimiento: date, pais_emision: str, id_pasajero: int, id_tipo_documento: int) -> None:
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