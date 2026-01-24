from typing import Any
from src.DBManager import DBManager
from src.TablaManager import TablaManager

class AsignacionesVuelosManager(TablaManager):

    def __init__(self, db_manager: DBManager) -> None:
        super().__init__("asignaciones_vuelos", db_manager)

    def asignar_tripulacion(self):
        pass

    def cambiar_piloto(self):
        pass

    def cambiar_azafata(self):
        pass

    def cambiar_mecanico(self):
        pass