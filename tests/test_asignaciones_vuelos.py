import pytest, random
from src.managers import *
from src.tipos import *
from src.entidades import *
from src.querys import *
from src.columnas import *
from src.errores import *
from src.GeneradorDatos import GeneradorDatos

def registrar_vuelos(vuelos_manager: VuelosManager, vuelos: list[VueloBase], id_staff: int) -> None:
    for vuelo in vuelos:
        vuelos_manager.registrar_vuelo(id_staff, vuelo)

def generar_vuelos_validos(generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, cant: int, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB]) -> list[VueloBase]:
    vuelos_validos: list[VueloBase] = []

    while not len(vuelos_validos) == cant:
        vuelo_generado = generador_datos.generar_vuelos(1, rutas, aviones)[0]
        if vuelos_manager._verificar_avion(vuelo_generado.id_avion, vuelo_generado.id_ruta, vuelo_generado.fecha_partida_programada, vuelo_generado.fecha_arribo_programada):
            vuelos_validos.append(vuelo_generado)
    
    return vuelos_validos

def test_registrar_asignacion_vuelo_comandante(db_conectada: DBManager, generador_datos: GeneradorDatos, asignaciones_vuelos_manager: AsignacionesVuelosManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))
    comandantes_disponibles: list[int] = asignaciones_vuelos_manager._obtener_comandantes_disponibles(ultimo_vuelo_registrado.fecha_partida_programada, ultimo_vuelo_registrado.fecha_arribo_programada)

    fecha_inicio = ultimo_vuelo_registrado.fecha_partida_programada
    fecha_fin = ultimo_vuelo_registrado._fecha_arribo_programada
    id_rol = 1 # PIC (Pilot in command).
    id_comandante: int = random.choice(comandantes_disponibles)

    asignacion_vuelo = AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, ultimo_vuelo_registrado.id, id_comandante)

    asignaciones_vuelos_manager.asignar_comandante(id_staff, asignacion_vuelo, ultimo_vuelo_registrado)

    ultima_asignacion = AsignacionVueloDesdeDB(*db_conectada.consultar_ultima_fila("asignaciones_vuelos", COLUMNAS_ASIGNACIONES_VUELOS))

    assert ultima_asignacion.fecha_inicio == asignacion_vuelo.fecha_inicio
    assert ultima_asignacion.fecha_fin == asignacion_vuelo.fecha_fin
    assert ultima_asignacion.id_rol == asignacion_vuelo.id_rol
    assert ultima_asignacion.id_vuelo == asignacion_vuelo.id_vuelo
    assert ultima_asignacion.id_staff == asignacion_vuelo.id_staff

def test_registrar_asignacion_vuelo_copiloto(db_conectada: DBManager, generador_datos: GeneradorDatos, asignaciones_vuelos_manager: AsignacionesVuelosManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))
    copilotos_disponibles: list[int] = asignaciones_vuelos_manager._obtener_copilotos_disponibles(ultimo_vuelo_registrado.fecha_partida_programada, ultimo_vuelo_registrado.fecha_arribo_programada)

    fecha_inicio = ultimo_vuelo_registrado.fecha_partida_programada
    fecha_fin = ultimo_vuelo_registrado._fecha_arribo_programada
    id_rol = 2 # SIC (Second in command).
    id_copiloto: int = random.choice(copilotos_disponibles)

    asignacion_vuelo = AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, ultimo_vuelo_registrado.id, id_copiloto)

    asignaciones_vuelos_manager.asignar_copiloto(id_staff, asignacion_vuelo, ultimo_vuelo_registrado)

    ultima_asignacion = AsignacionVueloDesdeDB(*db_conectada.consultar_ultima_fila("asignaciones_vuelos", COLUMNAS_ASIGNACIONES_VUELOS))

    assert ultima_asignacion.fecha_inicio == asignacion_vuelo.fecha_inicio
    assert ultima_asignacion.fecha_fin == asignacion_vuelo.fecha_fin
    assert ultima_asignacion.id_rol == asignacion_vuelo.id_rol
    assert ultima_asignacion.id_vuelo == asignacion_vuelo.id_vuelo
    assert ultima_asignacion.id_staff == asignacion_vuelo.id_staff

def test_registrar_asignacion_vuelo_auxiliar_vuelo(db_conectada: DBManager, generador_datos: GeneradorDatos, asignaciones_vuelos_manager: AsignacionesVuelosManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))
    auxiliares_vuelo_disponibles: list[int] = asignaciones_vuelos_manager._obtener_auxiliares_vuelo_disponibles(ultimo_vuelo_registrado.fecha_partida_programada, ultimo_vuelo_registrado.fecha_arribo_programada)

    fecha_inicio = ultimo_vuelo_registrado.fecha_partida_programada
    fecha_fin = ultimo_vuelo_registrado.fecha_arribo_programada
    id_rol = 3 # Auxiliar de vuelo.
    id_auxiliar_vuelo: int = random.choice(auxiliares_vuelo_disponibles)

    asignacion_vuelo = AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, ultimo_vuelo_registrado.id, id_auxiliar_vuelo)

    asignaciones_vuelos_manager.asignar_auxiliar_vuelo(id_staff, asignacion_vuelo, ultimo_vuelo_registrado)

    ultima_asignacion = AsignacionVueloDesdeDB(*db_conectada.consultar_ultima_fila("asignaciones_vuelos", COLUMNAS_ASIGNACIONES_VUELOS))

    assert ultima_asignacion.fecha_inicio == asignacion_vuelo.fecha_inicio
    assert ultima_asignacion.fecha_fin == asignacion_vuelo.fecha_fin
    assert ultima_asignacion.id_rol == asignacion_vuelo.id_rol
    assert ultima_asignacion.id_vuelo == asignacion_vuelo.id_vuelo
    assert ultima_asignacion.id_staff == asignacion_vuelo.id_staff

def test_registrar_asignacion_vuelo_supervisor_cabina(db_conectada: DBManager, generador_datos: GeneradorDatos, asignaciones_vuelos_manager: AsignacionesVuelosManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))
    supervisores_cabina_disponibles: list[int] = asignaciones_vuelos_manager._obtener_supervisores_cabina_disponibles(ultimo_vuelo_registrado.fecha_partida_programada, ultimo_vuelo_registrado.fecha_arribo_programada)

    fecha_inicio = ultimo_vuelo_registrado.fecha_partida_programada
    fecha_fin = ultimo_vuelo_registrado.fecha_arribo_programada
    id_rol = 4 # Supervisor de cabina.
    id_auxiliar_vuelo: int = random.choice(supervisores_cabina_disponibles)

    asignacion_vuelo = AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, ultimo_vuelo_registrado.id, id_auxiliar_vuelo)

    asignaciones_vuelos_manager.asignar_supervisor_cabina(id_staff, asignacion_vuelo, ultimo_vuelo_registrado)

    ultima_asignacion = AsignacionVueloDesdeDB(*db_conectada.consultar_ultima_fila("asignaciones_vuelos", COLUMNAS_ASIGNACIONES_VUELOS))

    assert ultima_asignacion.fecha_inicio == asignacion_vuelo.fecha_inicio
    assert ultima_asignacion.fecha_fin == asignacion_vuelo.fecha_fin
    assert ultima_asignacion.id_rol == asignacion_vuelo.id_rol
    assert ultima_asignacion.id_vuelo == asignacion_vuelo.id_vuelo
    assert ultima_asignacion.id_staff == asignacion_vuelo.id_staff

def test_registrar_asignacion_vuelo_mecanico(db_conectada: DBManager, generador_datos: GeneradorDatos, asignaciones_vuelos_manager: AsignacionesVuelosManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))
    mecanicos_disponibles: list[int] = asignaciones_vuelos_manager._obtener_mecanicos_disponibles(ultimo_vuelo_registrado.fecha_partida_programada, ultimo_vuelo_registrado.fecha_arribo_programada)

    fecha_inicio = ultimo_vuelo_registrado.fecha_partida_programada
    fecha_fin = ultimo_vuelo_registrado.fecha_arribo_programada
    id_rol = 7 # Supervisor de cabina.
    id_mecanico: int = random.choice(mecanicos_disponibles)

    asignacion_vuelo = AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, ultimo_vuelo_registrado.id, id_mecanico)

    asignaciones_vuelos_manager.asignar_mecanico(id_staff, asignacion_vuelo, ultimo_vuelo_registrado)

    ultima_asignacion = AsignacionVueloDesdeDB(*db_conectada.consultar_ultima_fila("asignaciones_vuelos", COLUMNAS_ASIGNACIONES_VUELOS))

    assert ultima_asignacion.fecha_inicio == asignacion_vuelo.fecha_inicio
    assert ultima_asignacion.fecha_fin == asignacion_vuelo.fecha_fin
    assert ultima_asignacion.id_rol == asignacion_vuelo.id_rol
    assert ultima_asignacion.id_vuelo == asignacion_vuelo.id_vuelo
    assert ultima_asignacion.id_staff == asignacion_vuelo.id_staff

def test_registrar_asignacion_vuelo_inspector(db_conectada: DBManager, generador_datos: GeneradorDatos, asignaciones_vuelos_manager: AsignacionesVuelosManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))
    inspectores_avion_disponibles: list[int] = asignaciones_vuelos_manager._obtener_mecanicos_disponibles(ultimo_vuelo_registrado.fecha_partida_programada, ultimo_vuelo_registrado.fecha_arribo_programada)

    fecha_inicio = ultimo_vuelo_registrado.fecha_partida_programada
    fecha_fin = ultimo_vuelo_registrado.fecha_arribo_programada
    id_rol = 10 # Inspector de aviones.
    id_inspector_avion: int = random.choice(inspectores_avion_disponibles)

    asignacion_vuelo = AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, ultimo_vuelo_registrado.id, id_inspector_avion)

    asignaciones_vuelos_manager.asignar_mecanico(id_staff, asignacion_vuelo, ultimo_vuelo_registrado)

    ultima_asignacion = AsignacionVueloDesdeDB(*db_conectada.consultar_ultima_fila("asignaciones_vuelos", COLUMNAS_ASIGNACIONES_VUELOS))

    assert ultima_asignacion.fecha_inicio == asignacion_vuelo.fecha_inicio
    assert ultima_asignacion.fecha_fin == asignacion_vuelo.fecha_fin
    assert ultima_asignacion.id_rol == asignacion_vuelo.id_rol
    assert ultima_asignacion.id_vuelo == asignacion_vuelo.id_vuelo
    assert ultima_asignacion.id_staff == asignacion_vuelo.id_staff

def test_registrar_asignacion_vuelo_agente_check_in(db_conectada: DBManager, generador_datos: GeneradorDatos, asignaciones_vuelos_manager: AsignacionesVuelosManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))
    agentes_check_in_disponibles: list[int] = asignaciones_vuelos_manager._obtener_agentes_disponibles(ultimo_vuelo_registrado.fecha_partida_programada, ultimo_vuelo_registrado.fecha_arribo_programada)

    fecha_inicio = ultimo_vuelo_registrado.fecha_partida_programada
    fecha_fin = ultimo_vuelo_registrado.fecha_arribo_programada
    id_rol = 5 # Agente de check in.
    id_agente_check_in: int = random.choice(agentes_check_in_disponibles)

    asignacion_vuelo = AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, ultimo_vuelo_registrado.id, id_agente_check_in)

    asignaciones_vuelos_manager.asignar_agente_check_in(id_staff, asignacion_vuelo, ultimo_vuelo_registrado)

    ultima_asignacion = AsignacionVueloDesdeDB(*db_conectada.consultar_ultima_fila("asignaciones_vuelos", COLUMNAS_ASIGNACIONES_VUELOS))

    assert ultima_asignacion.fecha_inicio == asignacion_vuelo.fecha_inicio
    assert ultima_asignacion.fecha_fin == asignacion_vuelo.fecha_fin
    assert ultima_asignacion.id_rol == asignacion_vuelo.id_rol
    assert ultima_asignacion.id_vuelo == asignacion_vuelo.id_vuelo
    assert ultima_asignacion.id_staff == asignacion_vuelo.id_staff

def test_registrar_asignacion_vuelo_agente_embarque(db_conectada: DBManager, generador_datos: GeneradorDatos, asignaciones_vuelos_manager: AsignacionesVuelosManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))
    agentes_embarque_disponibles: list[int] = asignaciones_vuelos_manager._obtener_agentes_disponibles(ultimo_vuelo_registrado.fecha_partida_programada, ultimo_vuelo_registrado.fecha_arribo_programada)

    fecha_inicio = ultimo_vuelo_registrado.fecha_partida_programada
    fecha_fin = ultimo_vuelo_registrado.fecha_arribo_programada
    id_rol = 6 # Agente de embarque.
    id_agente_embarque: int = random.choice(agentes_embarque_disponibles)

    asignacion_vuelo = AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, ultimo_vuelo_registrado.id, id_agente_embarque)

    asignaciones_vuelos_manager.asignar_agente_embarque(id_staff, asignacion_vuelo, ultimo_vuelo_registrado)

    ultima_asignacion = AsignacionVueloDesdeDB(*db_conectada.consultar_ultima_fila("asignaciones_vuelos", COLUMNAS_ASIGNACIONES_VUELOS))

    assert ultima_asignacion.fecha_inicio == asignacion_vuelo.fecha_inicio
    assert ultima_asignacion.fecha_fin == asignacion_vuelo.fecha_fin
    assert ultima_asignacion.id_rol == asignacion_vuelo.id_rol
    assert ultima_asignacion.id_vuelo == asignacion_vuelo.id_vuelo
    assert ultima_asignacion.id_staff == asignacion_vuelo.id_staff

def test_registrar_asignacion_vuelo_supervisor_agentes(db_conectada: DBManager, generador_datos: GeneradorDatos, asignaciones_vuelos_manager: AsignacionesVuelosManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))
    supervisor_agentes_disponibles: list[int] = asignaciones_vuelos_manager._obtener_supervisores_agentes_disponibles(ultimo_vuelo_registrado.fecha_partida_programada, ultimo_vuelo_registrado.fecha_arribo_programada)

    fecha_inicio = ultimo_vuelo_registrado.fecha_partida_programada
    fecha_fin = ultimo_vuelo_registrado.fecha_arribo_programada
    id_rol = 6 # Supervisor de agentes.
    id_supervisor_agente: int = random.choice(supervisor_agentes_disponibles)

    asignacion_vuelo = AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, ultimo_vuelo_registrado.id, id_supervisor_agente)

    asignaciones_vuelos_manager.asignar_supervisor_agentes(id_staff, asignacion_vuelo, ultimo_vuelo_registrado)

    ultima_asignacion = AsignacionVueloDesdeDB(*db_conectada.consultar_ultima_fila("asignaciones_vuelos", COLUMNAS_ASIGNACIONES_VUELOS))

    assert ultima_asignacion.fecha_inicio == asignacion_vuelo.fecha_inicio
    assert ultima_asignacion.fecha_fin == asignacion_vuelo.fecha_fin
    assert ultima_asignacion.id_rol == asignacion_vuelo.id_rol
    assert ultima_asignacion.id_vuelo == asignacion_vuelo.id_vuelo
    assert ultima_asignacion.id_staff == asignacion_vuelo.id_staff