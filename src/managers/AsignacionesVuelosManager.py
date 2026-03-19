from datetime import datetime
from src.managers.DBManager import DBManager
from src.managers.TablaManager import TablaManager
from src.entidades import AsignacionVueloBase
from src.querys import *
from src.errores import *

class AsignacionesVuelosManager(TablaManager):

    def __init__(self, db_manager: DBManager) -> None:
        super().__init__("asignaciones_vuelos", db_manager)

    def asignar_comandante(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_comandante: int) -> None:
        comandantes_disponibles: list[int] = self._obtener_comandantes_disponibles(fecha_inicio, fecha_fin)

        if id_comandante not in comandantes_disponibles:
            raise Exception(ERROR_COMANDANTE_INVALIDO)
        
        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 1, id_vuelo, id_comandante)

        super().agregar_fila(id_staff, asignacion)

    def asignar_copiloto(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_copiloto: int) -> None:
        copilotos_disponibles: list[int] = self._obtener_copilotos_disponibles(fecha_inicio, fecha_fin)

        if id_copiloto not in copilotos_disponibles:
            raise Exception(ERROR_COPILOTO_INVALIDO)
        
        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 2, id_vuelo, id_copiloto)

        super().agregar_fila(id_staff, asignacion)

    def asignar_auxiliar_vuelo(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_auxiliar_vuelo: int) -> None:
        auxiliares_vuelo_disponibles: list[int] = self._obtener_auxiliares_vuelo_disponibles(fecha_inicio, fecha_fin)

        if id_auxiliar_vuelo not in auxiliares_vuelo_disponibles:
            raise Exception(ERROR_AUXILIAR_VUELO_INVALIDO)
        
        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 3, id_vuelo, id_auxiliar_vuelo)

        super().agregar_fila(id_staff, asignacion)

    def asginar_supervisor_cabina(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_supervisor_cabina: int) -> None:
        supervisores_cabina_disponibles: list[int] = self._obtener_supervisores_cabina_disponibles(fecha_inicio, fecha_fin)

        if id_supervisor_cabina not in supervisores_cabina_disponibles:
            raise Exception(ERROR_SUPERVISOR_CABINA_INVALIDO)

        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 4, id_vuelo, id_supervisor_cabina)

        super().agregar_fila(id_staff, asignacion)

    def asignar_mecanico(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_mecanico: int) -> None:
        mecanicos_disponibles: list[int] = self._obtener_mecanicos_disponibles(fecha_inicio, fecha_fin)

        if id_mecanico not in mecanicos_disponibles:
            raise Exception(ERROR_MECANICO_INVALIDO)
        
        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 8, id_vuelo, id_staff)

        super().agregar_fila(id_staff, asignacion)

    def asignar_inspector(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_inspector: int) -> None:
        inspectores_disponibles: list[int] = []

        if id_inspector not in inspectores_disponibles:
            raise Exception(ERROR_INSPECTOR_INVALIDO)
        
        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 10, id_vuelo, id_inspector)

        super().agregar_fila(id_staff, asignacion)

    def asignar_agente_check_in(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_agente: int) -> None:
        agentes_disponibles: list[int] = self._obtener_agentes_disponibles(fecha_inicio, fecha_fin)

        if id_agente not in agentes_disponibles:
            raise Exception(ERROR_AGENTE_INVALIDO)
        
        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 5, id_vuelo, id_staff)

        super().agregar_fila(id_staff, asignacion)

    def asignar_agente_embarque(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_agente: int) -> None:
        agentes_disponibles: list[int] = self._obtener_agentes_disponibles(fecha_inicio, fecha_fin)

        if id_agente not in agentes_disponibles:
            raise Exception(ERROR_AGENTE_INVALIDO)
        
        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 6, id_vuelo, id_staff)

        super().agregar_fila(id_staff, asignacion)

    def asignar_supervisor_agentes(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_supervisor: int) -> None:
        supervisores_agentes_disponibles: list[int] = self._obtener_supervisores_agentes_disponibles(fecha_inicio, fecha_fin)

        if id_supervisor not in supervisores_agentes_disponibles:
            raise Exception(ERROR_SUVERVISOR_AGENTE_INVALIDO)

        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 7, id_vuelo, id_supervisor)

        super().agregar_fila(id_staff, asignacion)

    def _obtener_comandantes_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime) -> list[int]:
        query = OBTENER_COMANDANTES
        
        valores = (fecha_inicio, fecha_fin, fecha_fin)

        comandantes_disponibles: list[int] = self.db_manager.consultar_columna_unica(query, valores)
        
        return comandantes_disponibles
    
    def _obtener_copilotos_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime) -> list[int]:
        query = OBTENER_COPILOTOS

        valores = (fecha_inicio, fecha_fin, fecha_fin)

        copilotos_disponibles: list[int] = self.db_manager.consultar_columna_unica(query, valores)

        return copilotos_disponibles
    
    def _obtener_auxiliares_vuelo_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime) -> list[int]:
        query = OBTENER_AUXILIARES_VUELO
        
        valores = (fecha_inicio, fecha_fin, fecha_fin)

        auxiliares_vuelo_disponibles: list[int] = self.db_manager.consultar_columna_unica(query, valores)

        return auxiliares_vuelo_disponibles
    
    def _obtener_mecanicos_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime) -> list[int]:
        query = OBTENER_MECANICOS
        
        valores = (fecha_inicio, fecha_fin, fecha_fin)

        mecanicos_disponibles: list[int] = self.db_manager.consultar_columna_unica(query, valores)

        return mecanicos_disponibles

    def _obtener_agentes_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime) -> list[int]:
        query = OBTENER_AGENTES
        
        valores = (fecha_inicio, fecha_fin, fecha_fin)

        agentes_disponibles: list[int] = self.db_manager.consultar_columna_unica(query, valores)

        return agentes_disponibles
    
    def _obtener_inspectores_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime) -> list[int]:
        query = OBTENER_INSPECTORES
        
        valores = (fecha_inicio, fecha_fin, fecha_fin)

        inspectores_disponibles: list[int] = self.db_manager.consultar_columna_unica(query, valores)

        return inspectores_disponibles
    
    def _obtener_supervisores_agentes_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime) -> list[int]:
        query = OBTENER_SUPERVISORES_AGENTES
        
        valores = (fecha_inicio, fecha_fin, fecha_fin)

        supervisores_agentes_disponibles: list[int] = self.db_manager.consultar_columna_unica(query, valores)

        return supervisores_agentes_disponibles
    
    def _obtener_supervisores_cabina_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime) -> list[int]:
        query = OBTENER_SUPERVISORES_CABINA
        
        valores = (fecha_inicio, fecha_fin, fecha_fin)

        supervisores_cabina_disponibles: list[int] = self.db_manager.consultar_columna_unica(query, valores)

        return supervisores_cabina_disponibles