from datetime import datetime
from src.managers.DBManager import DBManager
from src.managers.TablaManager import TablaManager
from src.entidades import AsignacionVueloBase, VueloDesdeDB
from src.querys import *
from src.errores import *

class AsignacionesVuelosManager(TablaManager):

    def __init__(self, db_manager: DBManager) -> None:
        super().__init__("asignaciones_vuelos", db_manager)

    def asignar_comandante(self, id_staff: int, asignacion: AsignacionVueloBase, vuelo: VueloDesdeDB) -> None:
        comandantes_disponibles: list[int] = self._obtener_comandantes_disponibles(vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada)

        if asignacion.id_staff not in comandantes_disponibles:
            raise Exception(ERROR_COMANDANTE_INVALIDO)
        
        super().agregar_fila(id_staff, asignacion)

    def asignar_copiloto(self, id_staff: int, asignacion: AsignacionVueloBase, vuelo: VueloDesdeDB) -> None:
        copilotos_disponibles: list[int] = self._obtener_copilotos_disponibles(vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada)

        if asignacion.id_staff not in copilotos_disponibles:
            raise Exception(ERROR_COPILOTO_INVALIDO)
        
        super().agregar_fila(id_staff, asignacion)

    def asignar_auxiliar_vuelo(self, id_staff: int, asignacion: AsignacionVueloBase, vuelo: VueloDesdeDB) -> None:
        auxiliares_vuelo_disponibles: list[int] = self._obtener_auxiliares_vuelo_disponibles(vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada)

        if asignacion.id_staff not in auxiliares_vuelo_disponibles:
            raise Exception(ERROR_AUXILIAR_VUELO_INVALIDO)
        
        super().agregar_fila(id_staff, asignacion)

    def asignar_supervisor_cabina(self, id_staff: int, asignacion: AsignacionVueloBase, vuelo: VueloDesdeDB) -> None:
        supervisores_cabina_disponibles: list[int] = self._obtener_supervisores_cabina_disponibles(vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada)

        if asignacion.id_staff not in supervisores_cabina_disponibles:
            raise Exception(ERROR_SUPERVISOR_CABINA_INVALIDO)

        super().agregar_fila(id_staff, asignacion)

    def asignar_mecanico(self, id_staff: int, asignacion: AsignacionVueloBase, vuelo: VueloDesdeDB) -> None:
        mecanicos_disponibles: list[int] = self._obtener_mecanicos_disponibles(vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada)

        if asignacion.id_staff not in mecanicos_disponibles:
            raise Exception(ERROR_MECANICO_INVALIDO)
        
        super().agregar_fila(id_staff, asignacion)

    def asignar_inspector(self, id_staff: int, asignacion: AsignacionVueloBase, vuelo: VueloDesdeDB) -> None:
        inspectores_disponibles: list[int] = []

        if asignacion.id_staff not in inspectores_disponibles:
            raise Exception(ERROR_INSPECTOR_INVALIDO)
        
        super().agregar_fila(id_staff, asignacion)

    def asignar_agente_check_in(self, id_staff: int, asignacion: AsignacionVueloBase, vuelo: VueloDesdeDB) -> None:
        agentes_disponibles: list[int] = self._obtener_agentes_disponibles(vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada)

        if asignacion.id_staff not in agentes_disponibles:
            raise Exception(ERROR_AGENTE_INVALIDO)
        
        super().agregar_fila(id_staff, asignacion)

    def asignar_agente_embarque(self, id_staff: int, asignacion: AsignacionVueloBase, vuelo: VueloDesdeDB) -> None:
        agentes_disponibles: list[int] = self._obtener_agentes_disponibles(vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada)

        if asignacion.id_staff not in agentes_disponibles:
            raise Exception(ERROR_AGENTE_INVALIDO)
        
        super().agregar_fila(id_staff, asignacion)

    def asignar_supervisor_agentes(self, id_staff: int, asignacion: AsignacionVueloBase, vuelo: VueloDesdeDB) -> None:
        supervisores_agentes_disponibles: list[int] = self._obtener_supervisores_agentes_disponibles(vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada)

        if asignacion.id_staff not in supervisores_agentes_disponibles:
            raise Exception(ERROR_SUVERVISOR_AGENTE_INVALIDO)

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