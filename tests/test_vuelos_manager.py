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

def test_registrar_vuelo_correcto(db_conectada: DBManager, generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    assert ultimo_vuelo_registrado.id_ruta == vuelo.id_ruta
    assert ultimo_vuelo_registrado.id_avion == vuelo.id_avion
    assert ultimo_vuelo_registrado.id_estado_actual == vuelo.id_estado_actual
    assert ultimo_vuelo_registrado.fecha_partida_programada == vuelo.fecha_partida_programada
    assert ultimo_vuelo_registrado.fecha_arribo_programada == vuelo.fecha_arribo_programada
    assert ultimo_vuelo_registrado.costo_operativo_usd == vuelo.costo_operativo_usd
    assert ultimo_vuelo_registrado.precio_venta_usd == vuelo.precio_venta_usd

def test_registrar_vuelo_staff_invalido(generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB]) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]

    ID_STAFF = 999 # cambio el id_staff por uno erróneo.

    with pytest.raises(Exception, match=ERROR_STAFF_INVALIDO):
        vuelos_manager.registrar_vuelo(ID_STAFF, vuelo)

def test_registrar_vuelo_fecha_partida_programada_invalida(generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    pass

def test_registrar_vuelo_fecha_arribo_programada_invalida(generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    pass

def test_registrar_vuelo_avion_invalido(generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]

    vuelo.id_avion = 999 # cambio el id_avion por uno erróneo.

    with pytest.raises(Exception, match=ERROR_AVION_Y_RUTA_INVALIDAS):
        vuelos_manager.registrar_vuelo(id_staff, vuelo)

def test_modificar_vuelo_fechas_correctas(db_conectada: DBManager, generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    pass

def test_modificar_vuelo_fecha_partida_programada_invalida(db_conectada: DBManager, generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    pass

def test_modificar_vuelo_fecha_arribo_programada_invalida(db_conectada: DBManager, generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    pass

def test_modificar_vuelo_avion_correcto(db_conectada: DBManager, generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    nuevo_id_avion = random.choice(vuelos_manager._obtener_aviones_disponibles(vuelo.id_ruta, vuelo.fecha_partida_programada, vuelo.fecha_arribo_programada))
    
    vuelos_manager.modificar_avion(ultimo_vuelo_registrado, id_staff, nuevo_id_avion)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    assert ultimo_vuelo_registrado.id_ruta == vuelo.id_ruta
    assert ultimo_vuelo_registrado.id_avion == nuevo_id_avion
    assert ultimo_vuelo_registrado.id_estado_actual == vuelo.id_estado_actual
    assert ultimo_vuelo_registrado.fecha_partida_programada == vuelo.fecha_partida_programada
    assert ultimo_vuelo_registrado.fecha_arribo_programada == vuelo.fecha_arribo_programada
    assert ultimo_vuelo_registrado.costo_operativo_usd == vuelo.costo_operativo_usd
    assert ultimo_vuelo_registrado.precio_venta_usd == vuelo.precio_venta_usd

def test_modificar_vuelo_avion_invalido(db_conectada: DBManager, generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    nuevo_id_avion = 999 # cambio el id_avion por uno erróneo.
    
    with pytest.raises(Exception, match=ERROR_AVION_INVALIDO):
        vuelos_manager.modificar_avion(ultimo_vuelo_registrado, id_staff, nuevo_id_avion)

def test_modificar_vuelo_ruta_correcta(db_conectada: DBManager, generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    nuevo_id_ruta = random.choice(vuelos_manager._obtener_rutas_disponibles(vuelo.id_avion))
    while nuevo_id_ruta == vuelo.id_ruta:
        nuevo_id_ruta = random.choice(vuelos_manager._obtener_rutas_disponibles(vuelo.id_avion))

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    vuelos_manager.modificar_ruta(ultimo_vuelo_registrado, id_staff, nuevo_id_ruta)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))
    
    assert ultimo_vuelo_registrado.id_ruta == nuevo_id_ruta
    assert ultimo_vuelo_registrado.id_avion == vuelo.id_avion
    assert ultimo_vuelo_registrado.id_estado_actual == vuelo.id_estado_actual
    assert ultimo_vuelo_registrado.fecha_partida_programada == vuelo.fecha_partida_programada
    assert ultimo_vuelo_registrado.fecha_arribo_programada == vuelo.fecha_arribo_programada
    assert ultimo_vuelo_registrado.costo_operativo_usd == vuelo.costo_operativo_usd
    assert ultimo_vuelo_registrado.precio_venta_usd == vuelo.precio_venta_usd

def test_modificar_vuelo_ruta_invalida(db_conectada: DBManager, generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    nuevo_id_ruta = 999 # cambio el id_ruta por uno erróneo.
    
    with pytest.raises(Exception, match=ERROR_RUTA_INVALIDA):
        vuelos_manager.modificar_ruta(ultimo_vuelo_registrado, id_staff, nuevo_id_ruta)

def test_modificar_vuelo_estado_en_vuelo(db_conectada: DBManager, generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    nuevo_id_estado_actual = 2 # En vuelo.

    vuelos_manager.modificar_estado(ultimo_vuelo_registrado, id_staff, nuevo_id_estado_actual)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    assert ultimo_vuelo_registrado.id_ruta == vuelo.id_ruta
    assert ultimo_vuelo_registrado.id_avion == vuelo.id_avion
    assert ultimo_vuelo_registrado.id_estado_actual == nuevo_id_estado_actual
    assert ultimo_vuelo_registrado.fecha_partida_programada == vuelo.fecha_partida_programada
    assert ultimo_vuelo_registrado.fecha_arribo_programada == vuelo.fecha_arribo_programada
    assert ultimo_vuelo_registrado.fecha_partida_real != None
    assert ultimo_vuelo_registrado.fecha_arribo_real == None 
    assert ultimo_vuelo_registrado.costo_operativo_usd == vuelo.costo_operativo_usd
    assert ultimo_vuelo_registrado.precio_venta_usd == vuelo.precio_venta_usd

def test_modificar_vuelo_estado_aterrizado(db_conectada: DBManager, generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    nuevo_id_estado_actual = 2 # En vuelo.

    vuelos_manager.modificar_estado(ultimo_vuelo_registrado, id_staff, nuevo_id_estado_actual)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    nuevo_id_estado_actual = 3 # Aterrizado.

    vuelos_manager.modificar_estado(ultimo_vuelo_registrado, id_staff, nuevo_id_estado_actual)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    assert ultimo_vuelo_registrado.id_ruta == vuelo.id_ruta
    assert ultimo_vuelo_registrado.id_avion == vuelo.id_avion
    assert ultimo_vuelo_registrado.id_estado_actual == nuevo_id_estado_actual
    assert ultimo_vuelo_registrado.fecha_partida_programada == vuelo.fecha_partida_programada
    assert ultimo_vuelo_registrado.fecha_arribo_programada == vuelo.fecha_arribo_programada
    assert ultimo_vuelo_registrado.fecha_partida_real != None
    assert ultimo_vuelo_registrado.fecha_arribo_real != None 
    assert ultimo_vuelo_registrado.costo_operativo_usd == vuelo.costo_operativo_usd
    assert ultimo_vuelo_registrado.precio_venta_usd == vuelo.precio_venta_usd

def test_modificar_vuelo_estado_invalido(db_conectada: DBManager, generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    nuevo_id_estado_actual = 999 # cambio el id_estado_actual por uno erróneo.

    with pytest.raises(Exception, match=ERROR_ESTADO_INVALIDO):
        vuelos_manager.modificar_estado(ultimo_vuelo_registrado, id_staff, nuevo_id_estado_actual)