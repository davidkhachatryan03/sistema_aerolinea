from typing import Any
from src.DBManager import DBManager
from src.TablaManager import TablaManager

class AsignacionesVuelosManager(TablaManager):

    def __init__(self, db_manager: DBManager) -> None:
        super().__init__("asignaciones_vuelos", db_manager)

    def asignar_tripulacion(self):
        pass

    def asignar_piloto(self, id_staff: int, id_vuelo: int, id_piloto: int) -> None:
        pass

    def asignar_azafata(self):
        pass

    def asignar_mecanico(self):
        pass