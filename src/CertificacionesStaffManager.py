from src.entidades.CertificacionStaff import CertificacionStaff
from src.TablaManager import TablaManager
from datetime import datetime
from typing import Any

FilaCertificacion = tuple[int, str, datetime, int | None]

class CertificacionesStaffManager(TablaManager):

    def __init__(self, db_manager) -> None:
        super().__init__("certificaciones_staff", db_manager)
        self.campos_requeridos = ["id_staff", "descripcion", "licencia_hasta"]

    def registrar_certificacion(self, id_staff: int, certificacion: CertificacionStaff) -> None:
        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        if not self._verificar_campos_requeridos(certificacion):
            raise Exception("Error: no se ingresaron todos los campos requeridos.")
        
        datos: dict[str, Any] = certificacion.to_dict()
        
        super().agregar_fila(id_staff, datos)

    def modificar_id_staff(self, id_certificacion: int, id_staff_modifica: int, id_staff_nuevo: int) -> None:
        if not super()._verificar_id_a_modificar(id_certificacion):
            raise Exception("Error: el id a modificar no existe.")

        if not super()._verificar_id_staff(id_staff_modifica):
            raise Exception("Error: el staff ingresado no es válido.")
        
        if not super()._verificar_id_staff(id_staff_nuevo):
            raise Exception("Error: el staff ingresado no es válido.")
        
        certificacion: CertificacionStaff = self._obtener_documento(id_certificacion)

        if certificacion.id_staff == id_staff_nuevo:
            return
        
        super().modificar_fila(id_certificacion, id_staff_modifica, id_staff=id_staff_nuevo)

    def modificar_descripcion(self, id_certificacion: int, id_staff: int, descripcion: str) -> None:
        if not super()._verificar_id_a_modificar(id_certificacion):
            raise Exception("Error: el id a modificar no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        certificacion: CertificacionStaff = self._obtener_documento(id_certificacion)

        if certificacion.id_staff == id_staff:
            return
        
        super().modificar_fila(id_certificacion, id_staff, descripcion=descripcion)
        
    def modificar_vencimiento(self, id_certificacion: int, id_staff: int, licencia_hasta: datetime) -> None:
        if not super()._verificar_id_a_modificar(id_certificacion):
            raise Exception("Error: el id a modificar no existe.")

        if not super()._verificar_id_staff(id_staff):
            raise Exception("Error: el staff ingresado no es válido.")
        
        certificacion: CertificacionStaff = self._obtener_documento(id_certificacion)

        if certificacion.licencia_hasta == licencia_hasta:
            return
        
        super().modificar_fila(id_certificacion, id_staff, licencia_hasta=licencia_hasta)
    
    def _verificar_campos_requeridos(self, certificacion: CertificacionStaff):
        for campo in self.campos_requeridos:
            if getattr(certificacion, campo) == None:
                return False
        
        return True
    
    def _obtener_documento(self, id_certificacion: int) -> CertificacionStaff:
        query = """
                SELECT  id_staff,
                        descripcion,
                        licencia_hasta,
                        id
                FROM    certificaciones_staff
                WHERE   id = %s
                """
        
        consulta_certificacion: list[tuple] = self.db_manager.consultar(query, (id_certificacion,))

        if consulta_certificacion:
            fila_certificacion: FilaCertificacion = consulta_certificacion[0]
            certificacion = CertificacionStaff(*fila_certificacion)
        else:
            raise Exception("Error: no se encontró ningún resultado al consultar.")
        
        return certificacion