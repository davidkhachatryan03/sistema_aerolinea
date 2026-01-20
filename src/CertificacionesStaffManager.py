from src.entidades.CertificacionStaff import CertificacionStaff
from src.TablaManager import TablaManager
from typing import Any

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
    
    def _verificar_campos_requeridos(self, certificacion: CertificacionStaff):
        for campo in self.campos_requeridos:
            if getattr(certificacion, campo) == None:
                return False
        
        return True