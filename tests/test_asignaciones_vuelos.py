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

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))
    comandantes_disponibles: list[int] = asignaciones_vuelos_manager._obtener_comandantes_disponibles(ultimo_vuelo_registrado.fecha_partida_programada, ultimo_vuelo_registrado.fecha_arribo_programada)

    fecha_inicio = ultimo_vuelo_registrado.fecha_partida_programada
    fecha_fin = ultimo_vuelo_registrado._fecha_arribo_programada
    id_rol = 1 # PIC (Pilot in command)
    id_vuelo = ultimo_vuelo_registrado.id
    id_comandante: int = random.choice(comandantes_disponibles)

    asignacion_vuelo = AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, id_vuelo, id_comandante)

    asignaciones_vuelos_manager.asignar_comandante()