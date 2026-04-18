import pytest, random
from collections.abc import Callable
from src.managers import *
from src.tipos import *
from src.entidades import *
from src.querys import *
from src.columnas import *
from src.errores import *
from src.GeneradorDatos import GeneradorDatos

@pytest.mark.parametrize(
    "metodo_disponibles, metodo_asignar, id_rol",
    [
        ("_obtener_comandantes_disponibles", "asignar_comandante", 1),
        ("_obtener_copilotos_disponibles", "asignar_copiloto", 2),
        ("_obtener_auxiliares_vuelo_disponibles", "asignar_auxiliar_vuelo", 3),
        ("_obtener_supervisores_cabina_disponibles", "asignar_supervisor_cabina", 4),
        ("_obtener_agentes_disponibles", "asignar_agente_check_in", 5),
        ("_obtener_agentes_disponibles", "asignar_agente_embarque", 6),
        ("_obtener_mecanicos_disponibles", "asignar_mecanico", 7),
        ("_obtener_mecanicos_disponibles", "asignar_mecanico", 10), 
        ("_obtener_supervisores_agentes_disponibles", "asignar_supervisor_agentes", 6),
    ]
)
def test_registrar_asignacion_vuelo_todos_los_roles(db_conectada: DBManager, vuelo_registrado: Callable[[], tuple[VueloBase, VueloDesdeDB]], asignaciones_vuelos_manager: AsignacionesVuelosManager, id_staff: int, metodo_disponibles: str, metodo_asignar: str, id_rol: int) -> None:
    vuelo_valido_sin_registrar, ultimo_vuelo_registrado = vuelo_registrado()

    fecha_inicio = ultimo_vuelo_registrado.fecha_partida_programada
    fecha_fin = ultimo_vuelo_registrado.fecha_arribo_programada

    func_disponibles = getattr(asignaciones_vuelos_manager, metodo_disponibles)
    staff_disponible: list[int] = func_disponibles(fecha_inicio, fecha_fin)
    id_empleado_elegido: int = random.choice(staff_disponible)

    asignacion_vuelo = AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, ultimo_vuelo_registrado.id, id_empleado_elegido)

    func_asignar = getattr(asignaciones_vuelos_manager, metodo_asignar)
    func_asignar(id_staff, asignacion_vuelo, ultimo_vuelo_registrado)

    ultima_asignacion = AsignacionVueloDesdeDB(*db_conectada.consultar_ultima_fila("asignaciones_vuelos", COLUMNAS_ASIGNACIONES_VUELOS))

    assert ultima_asignacion.fecha_inicio == asignacion_vuelo.fecha_inicio
    assert ultima_asignacion.fecha_fin == asignacion_vuelo.fecha_fin
    assert ultima_asignacion.id_rol == asignacion_vuelo.id_rol
    assert ultima_asignacion.id_vuelo == asignacion_vuelo.id_vuelo
    assert ultima_asignacion.id_staff == asignacion_vuelo.id_staff