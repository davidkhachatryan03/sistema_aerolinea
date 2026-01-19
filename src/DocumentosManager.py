from src.TablaManager import TablaManager
from src.entidades.Documento import Documento
from datetime import datetime
from typing import Any

FilaDocumento = tuple[str, datetime, str, int, int, int]

class DocumentosManager(TablaManager):

    def __init__(self, db_manager) -> None:
        super().__init__("documentos", db_manager)

    # se podría hacer que se extraigan todos los datos a partir del numero de documento ingresado
    def registrar_documento(self, id_staff: int, documento: Documento) -> None:
        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        datos: dict[str, Any] = documento.to_dict()

        super().agregar_fila(id_staff, datos)

    def modificar_num_documento(self, id_documento: int, id_staff: int, num_documento: str) -> None:
        if not super()._verificar_id_a_modificar(id_documento):
            raise Exception("Error: el id a modificar no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        documento: Documento = self._obtener_documento(id_documento)

        if documento.num_documento == num_documento:
            return
        
        super().modificar_fila(id_documento, id_staff, num_documento=num_documento)
    
    def modificar_fecha_vencimiento(self, id_documento: int, id_staff: int, fecha_vencimiento: datetime) -> None:
        if not super()._verificar_id_a_modificar(id_documento):
            raise Exception("Error: el id a modificar no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        documento: Documento = self._obtener_documento(id_documento)
        
        if documento.fecha_vencimiento == fecha_vencimiento:
            return
        
        super().modificar_fila(id_documento, id_staff, fecha_vencimiento=fecha_vencimiento)

    def modificar_pais_emision(self, id_documento: int, id_staff: int, pais_emision: str) -> None:
        if not super()._verificar_id_a_modificar(id_documento):
            raise Exception("Error: el id a modificar no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        documento: Documento = self._obtener_documento(id_documento)

        if documento.pais_emision == pais_emision:
            return

        super().modificar_fila(id_documento, id_staff, pais_emision=pais_emision) 

    def modificar_id_pasajero(self, id_documento: int, id_staff: int, id_pasajero: int) -> None:
        if not super()._verificar_id_a_modificar(id_documento):
            raise Exception("Error: el id a modificar no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        documento: Documento = self._obtener_documento(id_documento)

        if documento.id_pasajero == id_pasajero:
            return

        super().modificar_fila(id_documento, id_staff, id_pasajero=id_pasajero)

    def modificar_id_tipo_documento(self, id_documento: int, id_staff: int, id_tipo_documento: int) -> None:
        if not super()._verificar_id_a_modificar(id_documento):
            raise Exception("Error: el id a modificar no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        documento: Documento = self._obtener_documento(id_documento)
        
        if documento.id_tipo_documento == id_tipo_documento:
            return

        super().modificar_fila(id_documento, id_staff, id_tipo_documento=id_tipo_documento)

    def _obtener_documento(self, id_documento: int) -> Documento:
        query = """
                SELECT  num_documento,
                        fecha_vencimiento,
                        pais_emision,
                        id_pasajero,
                        id_tipo_documento,
                        id
                FROM    documentos
                WHERE   id = %s
                """

        consulta_documento: FilaDocumento = self.db_manager.consultar(query, (id_documento, ))[0]

        if consulta_documento:
            documento = Documento(*consulta_documento)
        else:
            raise Exception("Error: el id ingresado no existe.")

        return documento