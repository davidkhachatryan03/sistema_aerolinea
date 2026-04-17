import pytest, random
from src.managers import *
from src.tipos import *
from src.entidades import *
from src.querys import *
from src.columnas import *
from src.errores import *
from src.GeneradorDatos import GeneradorDatos

def obtener_ultimo_vuelo_registrado(db_conectada: DBManager) -> VueloDesdeDB:
    return VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

def test_registrar_vuelo_correcto(vuelo_registrado: tuple[VueloBase, VueloDesdeDB]) -> None:
    vuelo_valido_sin_registrar, ultimo_vuelo_registrado = vuelo_registrado

    assert ultimo_vuelo_registrado.id_ruta == vuelo_valido_sin_registrar.id_ruta
    assert ultimo_vuelo_registrado.id_avion == vuelo_valido_sin_registrar.id_avion
    assert ultimo_vuelo_registrado.id_estado_actual == vuelo_valido_sin_registrar.id_estado_actual
    assert ultimo_vuelo_registrado.fecha_partida_programada == vuelo_valido_sin_registrar.fecha_partida_programada
    assert ultimo_vuelo_registrado.fecha_arribo_programada == vuelo_valido_sin_registrar.fecha_arribo_programada
    assert ultimo_vuelo_registrado.costo_operativo_usd == vuelo_valido_sin_registrar.costo_operativo_usd
    assert ultimo_vuelo_registrado.precio_venta_usd == vuelo_valido_sin_registrar.precio_venta_usd

def test_registrar_vuelo_staff_invalido(vuelo_registrado: tuple[VueloBase, VueloDesdeDB], vuelos_manager: VuelosManager) -> None:
    vuelo_valido_sin_registrar, ultimo_vuelo_registrado = vuelo_registrado

    ID_STAFF = 999 # cambio el id_staff por uno erróneo.

    with pytest.raises(Exception, match=ERROR_STAFF_INVALIDO):
        vuelos_manager.registrar_vuelo(ID_STAFF, vuelo_valido_sin_registrar)

def test_registrar_vuelo_fechas_invalidas(vuelo_registrado: tuple[VueloBase, VueloDesdeDB], vuelos_manager: VuelosManager, id_staff: int) -> None:
    vuelo_valido_sin_registrar, ultimo_vuelo_registrado = vuelo_registrado

    nueva_fecha_partida_programada = datetime(2080,1,1)
    nueva_fecha_arribo_programada = datetime(2070,1,1)

    with pytest.raises(Exception, match=ERROR_FECHAS_INVALIDAS):
        vuelos_manager.modificar_fechas(ultimo_vuelo_registrado, id_staff, nueva_fecha_partida_programada, nueva_fecha_arribo_programada)

def test_registrar_vuelo_avion_invalido(vuelo_registrado: tuple[VueloBase, VueloDesdeDB], vuelos_manager: VuelosManager, id_staff: int) -> None:
    vuelo_valido_sin_registrar, ultimo_vuelo_registrado = vuelo_registrado

    vuelo_valido_sin_registrar.id_avion = 999 # cambio el id_avion por uno erróneo.

    with pytest.raises(Exception, match=ERROR_AVION_Y_RUTA_INVALIDAS):
        vuelos_manager.registrar_vuelo(id_staff, vuelo_valido_sin_registrar)

def test_modificar_vuelo_fechas_correctas(db_conectada: DBManager, vuelo_registrado: tuple[VueloBase, VueloDesdeDB], vuelos_manager: VuelosManager, id_staff: int) -> None:
    vuelo_valido_sin_registrar, ultimo_vuelo_registrado = vuelo_registrado

    nueva_fecha_partida_programada = datetime(2080,1,1)
    nueva_fecha_arribo_programada = datetime(2080,1,2)

    vuelos_manager.modificar_fechas(ultimo_vuelo_registrado, id_staff, nueva_fecha_partida_programada, nueva_fecha_arribo_programada)

    ultimo_vuelo_registrado_modificado = obtener_ultimo_vuelo_registrado(db_conectada)

    assert ultimo_vuelo_registrado_modificado.id_ruta == ultimo_vuelo_registrado.id_ruta
    assert ultimo_vuelo_registrado_modificado.id_avion == ultimo_vuelo_registrado.id_avion
    assert ultimo_vuelo_registrado_modificado.id_estado_actual == ultimo_vuelo_registrado.id_estado_actual
    assert ultimo_vuelo_registrado_modificado.fecha_partida_programada == nueva_fecha_partida_programada
    assert ultimo_vuelo_registrado_modificado.fecha_arribo_programada == nueva_fecha_arribo_programada
    assert ultimo_vuelo_registrado_modificado.costo_operativo_usd == ultimo_vuelo_registrado.costo_operativo_usd
    assert ultimo_vuelo_registrado_modificado.precio_venta_usd == ultimo_vuelo_registrado.precio_venta_usd

def test_modificar_vuelo_avion_correcto(db_conectada: DBManager, vuelo_registrado: tuple[VueloBase, VueloDesdeDB], vuelos_manager: VuelosManager, id_staff: int) -> None:
    vuelo_valido_sin_registrar, ultimo_vuelo_registrado = vuelo_registrado

    nuevo_id_avion = random.choice(vuelos_manager._obtener_aviones_disponibles(ultimo_vuelo_registrado.id_ruta, ultimo_vuelo_registrado.fecha_partida_programada, ultimo_vuelo_registrado.fecha_arribo_programada))
    
    vuelos_manager.modificar_avion(ultimo_vuelo_registrado, id_staff, nuevo_id_avion)

    ultimo_vuelo_registrado_modificado = obtener_ultimo_vuelo_registrado(db_conectada)

    assert ultimo_vuelo_registrado_modificado.id_ruta == ultimo_vuelo_registrado.id_ruta
    assert ultimo_vuelo_registrado_modificado.id_avion == nuevo_id_avion
    assert ultimo_vuelo_registrado_modificado.id_estado_actual == ultimo_vuelo_registrado.id_estado_actual
    assert ultimo_vuelo_registrado_modificado.fecha_partida_programada == ultimo_vuelo_registrado.fecha_partida_programada
    assert ultimo_vuelo_registrado_modificado.fecha_arribo_programada == ultimo_vuelo_registrado.fecha_arribo_programada
    assert ultimo_vuelo_registrado_modificado.costo_operativo_usd == ultimo_vuelo_registrado.costo_operativo_usd
    assert ultimo_vuelo_registrado_modificado.precio_venta_usd == ultimo_vuelo_registrado.precio_venta_usd

def test_modificar_vuelo_avion_invalido(vuelo_registrado: tuple[VueloBase, VueloDesdeDB], vuelos_manager: VuelosManager, id_staff: int) -> None:
    vuelo_valido_sin_registrar, ultimo_vuelo_registrado = vuelo_registrado

    nuevo_id_avion = 999 # cambio el id_avion por uno erróneo.
    
    with pytest.raises(Exception, match=ERROR_AVION_INVALIDO):
        vuelos_manager.modificar_avion(ultimo_vuelo_registrado, id_staff, nuevo_id_avion)

def test_modificar_vuelo_ruta_correcta(db_conectada: DBManager, vuelo_registrado: tuple[VueloBase, VueloDesdeDB], vuelos_manager: VuelosManager, id_staff: int) -> None:
    vuelo_valido_sin_registrar, ultimo_vuelo_registrado = vuelo_registrado

    nuevo_id_ruta = random.choice(vuelos_manager._obtener_rutas_disponibles(ultimo_vuelo_registrado.id_avion))
    while nuevo_id_ruta == ultimo_vuelo_registrado.id_ruta:
        nuevo_id_ruta = random.choice(vuelos_manager._obtener_rutas_disponibles(ultimo_vuelo_registrado.id_avion))

    vuelos_manager.modificar_ruta(ultimo_vuelo_registrado, id_staff, nuevo_id_ruta)

    ultimo_vuelo_registrado_modificado = obtener_ultimo_vuelo_registrado(db_conectada)
    
    assert ultimo_vuelo_registrado_modificado.id_ruta == nuevo_id_ruta
    assert ultimo_vuelo_registrado_modificado.id_avion == ultimo_vuelo_registrado.id_avion
    assert ultimo_vuelo_registrado_modificado.id_estado_actual == ultimo_vuelo_registrado.id_estado_actual
    assert ultimo_vuelo_registrado_modificado.fecha_partida_programada == ultimo_vuelo_registrado.fecha_partida_programada
    assert ultimo_vuelo_registrado_modificado.fecha_arribo_programada == ultimo_vuelo_registrado.fecha_arribo_programada
    assert ultimo_vuelo_registrado_modificado.costo_operativo_usd == ultimo_vuelo_registrado.costo_operativo_usd
    assert ultimo_vuelo_registrado_modificado.precio_venta_usd == ultimo_vuelo_registrado.precio_venta_usd

def test_modificar_vuelo_ruta_invalida(vuelo_registrado: tuple[VueloBase, VueloDesdeDB], vuelos_manager: VuelosManager, id_staff: int) -> None:
    vuelo_valido_sin_registrar, ultimo_vuelo_registrado = vuelo_registrado

    nuevo_id_ruta = 999 # cambio el id_ruta por uno erróneo.
    
    with pytest.raises(Exception, match=ERROR_RUTA_INVALIDA):
        vuelos_manager.modificar_ruta(ultimo_vuelo_registrado, id_staff, nuevo_id_ruta)

def test_modificar_vuelo_estado_en_vuelo(db_conectada: DBManager, vuelo_registrado: tuple[VueloBase, VueloDesdeDB], vuelos_manager: VuelosManager, id_staff: int) -> None:
    vuelo_valido_sin_registrar, ultimo_vuelo_registrado = vuelo_registrado

    nuevo_id_estado_actual = 2 # En vuelo.

    vuelos_manager.modificar_estado(ultimo_vuelo_registrado, id_staff, nuevo_id_estado_actual)

    ultimo_vuelo_registrado_modificado = obtener_ultimo_vuelo_registrado(db_conectada)

    assert ultimo_vuelo_registrado_modificado.id_ruta == ultimo_vuelo_registrado.id_ruta
    assert ultimo_vuelo_registrado_modificado.id_avion == ultimo_vuelo_registrado.id_avion
    assert ultimo_vuelo_registrado_modificado.id_estado_actual == nuevo_id_estado_actual
    assert ultimo_vuelo_registrado_modificado.fecha_partida_programada == ultimo_vuelo_registrado.fecha_partida_programada
    assert ultimo_vuelo_registrado_modificado.fecha_arribo_programada == ultimo_vuelo_registrado.fecha_arribo_programada
    assert ultimo_vuelo_registrado_modificado.fecha_partida_real != None
    assert ultimo_vuelo_registrado_modificado.fecha_arribo_real == None 
    assert ultimo_vuelo_registrado_modificado.costo_operativo_usd == ultimo_vuelo_registrado.costo_operativo_usd
    assert ultimo_vuelo_registrado_modificado.precio_venta_usd == ultimo_vuelo_registrado.precio_venta_usd

def test_modificar_vuelo_estado_aterrizado(db_conectada: DBManager, vuelo_registrado: tuple[VueloBase, VueloDesdeDB], vuelos_manager: VuelosManager, id_staff: int) -> None:
    vuelo_valido_sin_registrar, ultimo_vuelo_registrado = vuelo_registrado

    nuevo_id_estado_actual = 2 # En vuelo.

    vuelos_manager.modificar_estado(ultimo_vuelo_registrado, id_staff, nuevo_id_estado_actual)

    ultimo_vuelo_registrado = obtener_ultimo_vuelo_registrado(db_conectada)

    nuevo_id_estado_actual = 3 # Aterrizado.

    vuelos_manager.modificar_estado(ultimo_vuelo_registrado, id_staff, nuevo_id_estado_actual)

    ultimo_vuelo_registrado_modificado = obtener_ultimo_vuelo_registrado(db_conectada)

    assert ultimo_vuelo_registrado_modificado.id_ruta == ultimo_vuelo_registrado.id_ruta
    assert ultimo_vuelo_registrado_modificado.id_avion == ultimo_vuelo_registrado.id_avion
    assert ultimo_vuelo_registrado_modificado.id_estado_actual == nuevo_id_estado_actual
    assert ultimo_vuelo_registrado_modificado.fecha_partida_programada == ultimo_vuelo_registrado.fecha_partida_programada
    assert ultimo_vuelo_registrado_modificado.fecha_arribo_programada == ultimo_vuelo_registrado.fecha_arribo_programada
    assert ultimo_vuelo_registrado_modificado.fecha_partida_real != None
    assert ultimo_vuelo_registrado_modificado.fecha_arribo_real != None 
    assert ultimo_vuelo_registrado_modificado.costo_operativo_usd == ultimo_vuelo_registrado.costo_operativo_usd
    assert ultimo_vuelo_registrado_modificado.precio_venta_usd == ultimo_vuelo_registrado.precio_venta_usd

def test_modificar_vuelo_estado_invalido(db_conectada: DBManager, vuelo_registrado: tuple[VueloBase, VueloDesdeDB], vuelos_manager: VuelosManager, id_staff: int) -> None:
    vuelo_valido_sin_registrar, ultimo_vuelo_registrado = vuelo_registrado
    
    nuevo_id_estado_actual = 999 # cambio el id_estado_actual por uno erróneo.

    with pytest.raises(Exception, match=ERROR_ESTADO_INVALIDO):
        vuelos_manager.modificar_estado(ultimo_vuelo_registrado, id_staff, nuevo_id_estado_actual)