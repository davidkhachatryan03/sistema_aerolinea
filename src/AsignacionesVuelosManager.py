from typing import Any
from datetime import datetime
from src.DBManager import DBManager
from src.TablaManager import TablaManager
from src.entidades.AsignacionVuelo import AsignacionVueloBase, AsignacionVueloDesdeDB

class AsignacionesVuelosManager(TablaManager):

    def __init__(self, db_manager: DBManager) -> None:
        super().__init__("asignaciones_vuelos", db_manager)

    def asignar_comandante(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_comandante: int) -> None:
        comandantes_disponibles: list[int] = self._obtener_comandantes_disponibles(fecha_inicio, fecha_fin)

        if id_comandante not in comandantes_disponibles:
            raise Exception("Error: el comandante ingresado no es válido.")
        
        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 1, id_vuelo, id_comandante)

        super().agregar_fila(id_staff, asignacion.to_dict())

    def asignar_copiloto(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_copiloto: int) -> None:
        copilotos_disponibles: list[int] = self._obtener_copilotos_disponibles(fecha_inicio, fecha_fin)

        if id_copiloto not in copilotos_disponibles:
            raise Exception("Error: el copiloto ingresado no es válido.")
        
        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 2, id_vuelo, id_copiloto)

        super().agregar_fila(id_staff, asignacion.to_dict())

    def asignar_auxiliar_vuelo(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_auxiliar_vuelo: int) -> None:
        auxiliares_vuelo_disponibles: list[int] = self._obtener_auxiliares_vuelo_disponibles(fecha_inicio, fecha_fin)

        if id_auxiliar_vuelo not in auxiliares_vuelo_disponibles:
            raise Exception("Error: el tripulante de cabina ingresado no es válido.")
        
        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 3, id_vuelo, id_auxiliar_vuelo)

        super().agregar_fila(id_staff, asignacion.to_dict())

    def asginar_supervisor_cabina(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_supervisor_cabina: int) -> None:
        supervisores_cabina_disponibles: list[int] = self._obtener_supervisores_cabina_disponibles(fecha_inicio, fecha_fin)

        if id_supervisor_cabina not in supervisores_cabina_disponibles:
            raise Exception("Error: el supervisor de cabina ingresado no es válido.")

        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 4, id_vuelo, id_supervisor_cabina)

        super().agregar_fila(id_staff, asignacion.to_dict())

    def asignar_mecanico(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_mecanico: int) -> None:
        mecanicos_disponibles: list[int] = self._obtener_mecanicos_disponibles(fecha_inicio, fecha_fin)

        if id_mecanico not in mecanicos_disponibles:
            raise Exception("Error: el mecánico ingresado no es válido.")
        
        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 8, id_vuelo, id_staff)

        super().agregar_fila(id_staff, asignacion.to_dict())

    def asignar_inspector(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_inspector: int) -> None:
        inspectores_disponibles: list[int] = []

        if id_inspector not in inspectores_disponibles:
            raise Exception("Error: el inspector ingresado no es válido.")
        
        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 10, id_vuelo, id_inspector)

        super().agregar_fila(id_staff, asignacion.to_dict())

    def asignar_agente_check_in(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_agente: int) -> None:
        agentes_disponibles: list[int] = self._obtener_agentes_disponibles(fecha_inicio, fecha_fin)

        if id_agente not in agentes_disponibles:
            raise Exception("Error: el agente ingresado no es válido.")
        
        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 5, id_vuelo, id_staff)

        super().agregar_fila(id_staff, asignacion.to_dict())

    def asignar_agente_embarque(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_agente: int) -> None:
        agentes_disponibles: list[int] = self._obtener_agentes_disponibles(fecha_inicio, fecha_fin)

        if id_agente not in agentes_disponibles:
            raise Exception("Error: el agente ingresado no es válido.")
        
        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 6, id_vuelo, id_staff)

        super().agregar_fila(id_staff, asignacion.to_dict())

    def asignar_supervisor_agentes(self, id_staff: int, fecha_inicio: datetime, fecha_fin: datetime, id_vuelo: int, id_supervisor: int) -> None:
        supervisores_agentes_disponibles: list[int] = self._obtener_supervisores_agentes_disponibles(fecha_inicio, fecha_fin)

        if id_supervisor not in supervisores_agentes_disponibles:
            raise Exception("Error: el supervisor ingresado no es válido.")

        asignacion = AsignacionVueloBase(fecha_inicio, fecha_fin, 7, id_vuelo, id_supervisor)

        super().agregar_fila(id_staff, asignacion.to_dict( ))


    def _obtener_comandantes_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime) -> list[int]:
        comandantes: list[int] = []

        query = """
                SELECT  s.id
                FROM    staff s
                WHERE   s.id NOT IN (
                    SELECT  av.id_staff
                    FROM    asignaciones_vuelos av
                    JOIN    vuelos v 
                    ON      av.id_vuelo = v.id
                    WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                    AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                )
                AND     s.id IN (
                        SELECT  cs.id_staff
                        FROM    certificaciones_staff cs
                        WHERE   cs.licencia_hasta >= %s
                )
                AND     s.id_cargo_actual = 1
                AND     s.id_estado_actual = 1;
                """
        
        valores = (fecha_inicio, fecha_fin, fecha_fin)

        consulta_comandantes_disponibles: list[tuple] = self.db_manager.consultar(query, valores)

        for comandante in consulta_comandantes_disponibles:
            comandantes.append(comandante[0])
        
        return comandantes
    
    def _obtener_copilotos_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime) -> list[int]:
        copilotos_disponibles: list[int] = []

        query = """
                SELECT  s.id
                FROM    staff s
                WHERE   s.id NOT IN (
                    SELECT  av.id_staff
                    FROM    asignaciones_vuelos av
                    JOIN    vuelos v 
                    ON      av.id_vuelo = v.id
                    WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                    AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                )
                AND     s.id IN (
                        SELECT  cs.id_staff
                        FROM    certificaciones_staff cs
                        WHERE   cs.licencia_hasta >= %s
                )
                AND     s.id_cargo_actual = 2
                AND     s.id_estado_actual = 1;
                """

        valores = (fecha_inicio, fecha_fin, fecha_fin)

        consulta_copilotos_disponibles: list[tuple] = self.db_manager.consultar(query, valores)

        for copiloto in consulta_copilotos_disponibles:
            copilotos_disponibles.append(copiloto[0])
        
        return copilotos_disponibles
    
    def _obtener_auxiliares_vuelo_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime) -> list[int]:
        auxiliares_vuelo_disponibles: list[int] = []

        query = """
                SELECT  s.id
                FROM    staff s
                WHERE   s.id NOT IN (
                    SELECT  av.id_staff
                    FROM    asignaciones_vuelos av
                    JOIN    vuelos v 
                    ON      av.id_vuelo = v.id
                    WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                    AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                )
                AND     s.id IN (
                        SELECT  cs.id_staff
                        FROM    certificaciones_staff cs
                        WHERE   cs.licencia_hasta >= %s
                )
                AND     s.id_cargo_actual = 3
                AND     s.id_estado_actual = 1;
                """
        
        valores = (fecha_inicio, fecha_fin, fecha_fin)

        consulta_auxiliares_vuelo_disponibles: list[tuple] = self.db_manager.consultar(query, valores)

        for auxiliar_vuelo in consulta_auxiliares_vuelo_disponibles:
            auxiliares_vuelo_disponibles.append(auxiliar_vuelo[0])

        return auxiliares_vuelo_disponibles
    
    def _obtener_mecanicos_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime) -> list[int]:
        mecanicos_disponibles: list[int] = []

        query = """
                SELECT  s.id
                FROM    staff s
                WHERE   s.id NOT IN (
                    SELECT  av.id_staff
                    FROM    asignaciones_vuelos av
                    JOIN    vuelos v 
                    ON      av.id_vuelo = v.id
                    WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                    AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                )
                AND     s.id IN (
                        SELECT  cs.id_staff
                        FROM    certificaciones_staff cs
                        WHERE   cs.licencia_hasta >= %s
                )
                AND     s.id_cargo_actual = 5
                AND     s.id_estado_actual = 1;
                """
        
        valores = (fecha_inicio, fecha_fin, fecha_fin)

        consulta_mecanicos_disponibles: list[tuple] = self.db_manager.consultar(query, valores)

        for mecanico in consulta_mecanicos_disponibles:
            mecanicos_disponibles.append(mecanico[0])

        return mecanicos_disponibles

    def _obtener_agentes_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime) -> list[int]:
        agentes_disponibles: list[int] = []

        query = """
                SELECT  s.id
                FROM    staff s
                WHERE   s.id NOT IN (
                    SELECT  av.id_staff
                    FROM    asignaciones_vuelos av
                    JOIN    vuelos v 
                    ON      av.id_vuelo = v.id
                    WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                    AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                )
                AND     s.id IN (
                        SELECT  cs.id_staff
                        FROM    certificaciones_staff cs
                        WHERE   cs.licencia_hasta >= %s
                )
                AND     s.id_cargo_actual = 7
                AND     s.id_estado_actual = 1;
                """
        
        valores = (fecha_inicio, fecha_fin, fecha_fin)

        consulta_agentes_disponibles: list[tuple] = self.db_manager.consultar(query, valores)

        for agente in consulta_agentes_disponibles:
            agentes_disponibles.append(agente[0])

        return agentes_disponibles
    
    def _obtener_inspectores_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime) -> list[int]:
        inspectores_disponibles: list[int] = []

        query = """
                SELECT  s.id
                FROM    staff s
                WHERE   s.id NOT IN (
                    SELECT  av.id_staff
                    FROM    asignaciones_vuelos av
                    JOIN    vuelos v 
                    ON      av.id_vuelo = v.id
                    WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                    AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                )
                AND     s.id IN (
                        SELECT  cs.id_staff
                        FROM    certificaciones_staff cs
                        WHERE   cs.licencia_hasta >= %s
                )
                AND     s.id_cargo_actual = 6
                AND     s.id_estado_actual = 1;
                """
        
        valores = (fecha_inicio, fecha_fin, fecha_fin)

        consulta_inspectores_disponibles: list[tuple] = self.db_manager.consultar(query, valores)

        for inspector in consulta_inspectores_disponibles:
            inspectores_disponibles.append(inspector[0])

        return inspectores_disponibles
    
    def _obtener_supervisores_agentes_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime) -> list[int]:
        supervisores_agentes_disponibles: list[int] = []

        query = """
                SELECT  s.id
                FROM    staff s
                WHERE   s.id NOT IN (
                    SELECT  av.id_staff
                    FROM    asignaciones_vuelos av
                    JOIN    vuelos v 
                    ON      av.id_vuelo = v.id
                    WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                    AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                )
                AND     s.id IN (
                        SELECT  cs.id_staff
                        FROM    certificaciones_staff cs
                        WHERE   cs.licencia_hasta >= %s
                )
                AND     s.id_cargo_actual = 8
                AND     s.id_estado_actual = 1;
                """
        
        valores = (fecha_inicio, fecha_fin, fecha_fin)

        consulta_supervisores_agentes_disponibles: list[tuple] = self.db_manager.consultar(query, valores)

        for supersor_agente in consulta_supervisores_agentes_disponibles:
            supervisores_agentes_disponibles.append(supersor_agente[0])

        return supervisores_agentes_disponibles
    
    def _obtener_supervisores_cabina_disponibles(self, fecha_inicio: datetime, fecha_fin: datetime) -> list[int]:
        supervisores_cabina_disponibles: list[int] = []

        query = """
                SELECT  s.id
                FROM    staff s
                WHERE   s.id NOT IN (
                    SELECT  av.id_staff
                    FROM    asignaciones_vuelos av
                    JOIN    vuelos v 
                    ON      av.id_vuelo = v.id
                    WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                    AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                )
                AND     s.id IN (
                        SELECT  cs.id_staff
                        FROM    certificaciones_staff cs
                        WHERE   cs.licencia_hasta >= %s
                )
                AND     s.id_cargo_actual = 4
                AND     s.id_estado_actual = 1;
                """
        
        valores = (fecha_inicio, fecha_fin, fecha_fin)

        consulta_supervisores_cabina_disponibles: list[tuple] = self.db_manager.consultar(query, valores)
        
        for supervisor_cabina in consulta_supervisores_cabina_disponibles:
            supervisores_cabina_disponibles.append(supervisor_cabina[0])

        return supervisores_cabina_disponibles