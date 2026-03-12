import pytest, os, random
from init_db import main
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, date
from src.entidades import *
from src.managers import *
from src.tipos import *
from src.errores import *

main()

@pytest.fixture
def db_conectada():
    db_manager = DBManager()
    db_manager.conectar()
    db_manager.execute("USE aerolinea")
    yield db_manager
    db_manager.desconectar()

def elegir_vuelo_valido(db_conectada: DBManager, ventas_manager: VentasManager):
    id_vuelo = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM vuelos LIMIT 10"))

    while not ventas_manager._verificar_capacidad(id_vuelo):
        id_vuelo = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM vuelos LIMIT 10"))
    
    return id_vuelo

def elegir_avion_valido(db_conectada: DBManager, id_ruta: int, fecha_partida_programada: datetime, fecha_arribo_programada: datetime, vuelos_manager: VuelosManager):
    id_avion = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM aviones LIMIT 10"))

    while not vuelos_manager._verificar_avion(id_avion, id_ruta, fecha_partida_programada, fecha_arribo_programada):
        id_avion = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM aviones LIMIT 10"))

    return id_avion

def elegir_ruta_valida(id_avion: int, id_ruta_actual: int, vuelos_manager: VuelosManager):
    nuevo_id_ruta = random.choice(vuelos_manager._obtener_rutas_disponibles(id_avion))

    while nuevo_id_ruta == id_ruta_actual:
        nuevo_id_ruta = random.choice(vuelos_manager._obtener_rutas_disponibles(id_avion))
    
    return nuevo_id_ruta

def test_registrar_venta_correcta(db_conectada: DBManager):
        ventas_manager = VentasManager(db_conectada)
        ID_STAFF = 25

        id_pasajero = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))
        id_vuelo = elegir_vuelo_valido(db_conectada, ventas_manager)
        num_reserva = "AAA123" # se genera aleatoriamente al registrarse la venta
        precio_pagado_usd = ventas_manager._obtener_precio_pagado_usd(id_vuelo)
        id_estado_actual = 3 # siempre se asigna este valor al registrar una venta

        venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)
        ventas_manager.registrar_venta(ID_STAFF, venta)

        consulta_venta: list[FilaVenta] = db_conectada.consultar("SELECT id, num_reserva, fecha_venta, precio_pagado_usd, id_vuelo, id_estado_actual, id_pasajero FROM ventas ORDER BY id DESC LIMIT 1")
        venta = VentaDesdeDB(*consulta_venta[0])

        assert venta.id_pasajero == id_pasajero
        assert venta.id_vuelo == id_vuelo
        assert len(venta.num_reserva) == 6 and type(venta.num_reserva) == str # solo reviso que el formato sea correcto
        assert venta.precio_pagado_usd == precio_pagado_usd
        assert venta.id_estado_actual == id_estado_actual
    
def test_registrar_venta_id_staff_invalido(db_conectada: DBManager):
    ventas_manager = VentasManager(db_conectada)
    ID_STAFF = 9999
    
    id_pasajero = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))
    id_vuelo = elegir_vuelo_valido(db_conectada, ventas_manager)
    num_reserva = "AAA123" # se genera aleatoriamente al registrarse la venta
    precio_pagado_usd = ventas_manager._obtener_precio_pagado_usd(id_vuelo)
    id_estado_actual = 3 # siempre se asigna este valor al registrar una venta

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

    with pytest.raises(Exception, match=ERROR_STAFF_INVALIDO):
        ventas_manager.registrar_venta(ID_STAFF, venta)
    
def test_registrar_venta_pasajero_invalido(db_conectada: DBManager):
    ventas_manager = VentasManager(db_conectada)
    ID_STAFF = 25

    id_pasajero = 9999
    id_vuelo = elegir_vuelo_valido(db_conectada, ventas_manager)
    num_reserva = "AAA123" # se genera aleatoriamente al registrarse la venta
    precio_pagado_usd = ventas_manager._obtener_precio_pagado_usd(id_vuelo)
    id_estado_actual = 3 # siempre se asigna este valor al registrar una venta

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

    with pytest.raises(Exception, match=ERROR_PASAJERO_INVALIDO):
        ventas_manager.registrar_venta(ID_STAFF, venta)

def test_registrar_venta_vuelo_invalido(db_conectada: DBManager):
    ventas_manager = VentasManager(db_conectada)
    ID_STAFF = 25

    id_pasajero = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))
    id_vuelo = 9999
    num_reserva = "AAA123" # se genera aleatoriamente al registrarse la venta
    precio_pagado_usd = Decimal("1000.21") # invento un precio aleatorio para que no falle la búsqueda según id_vuelo
    id_estado_actual = 3 # siempre se asigna este valor al registrar una venta

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

    with pytest.raises(Exception, match=ERROR_VUELO_INVALIDO):
        ventas_manager.registrar_venta(ID_STAFF, venta)

def test_registrar_venta_vuelo_lleno(db_conectada: DBManager):
    ventas_manager = VentasManager(db_conectada)
    ID_STAFF = 25
    
    id_pasajero = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))
    id_vuelo = elegir_vuelo_valido(db_conectada, ventas_manager)
    num_reserva = "AAA123" # se genera aleatoriamente al registrarse la venta
    precio_pagado_usd = ventas_manager._obtener_precio_pagado_usd(id_vuelo)
    id_estado_actual = 3 # siempre se asigna este valor al registrar una venta

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

    while ventas_manager._verificar_capacidad(id_vuelo):
        ventas_manager.registrar_venta(ID_STAFF, venta)

    with pytest.raises(Exception, match=ERROR_SIN_ASIENTOS):
        ventas_manager.registrar_venta(ID_STAFF, venta)

def test_modificar_venta_id_estado_actual(db_conectada: DBManager):
    ventas_manager = VentasManager(db_conectada)
    ID_STAFF = 25

    id_pasajero = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))
    id_vuelo = elegir_vuelo_valido(db_conectada, ventas_manager)
    num_reserva = "AAA123" # se genera aleatoriamente al registrarse la venta
    precio_pagado_usd = ventas_manager._obtener_precio_pagado_usd(id_vuelo)
    id_estado_actual = 3 # siempre se asigna este valor al registrar una venta

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)
    ventas_manager.registrar_venta(ID_STAFF, venta)

    consulta_id_venta: list[int] = db_conectada.consultar_columna_unica("SELECT id FROM ventas ORDER BY id DESC LIMIT 1")
    id_venta = consulta_id_venta[0]

    nuevo_id_estado_actual = 2

    ventas_manager.modificar_estado(id_venta, ID_STAFF, nuevo_id_estado_actual)

    consulta_venta: list[FilaVenta] = db_conectada.consultar("SELECT id, num_reserva, fecha_venta, precio_pagado_usd, id_vuelo, id_estado_actual, id_pasajero FROM ventas ORDER BY id DESC LIMIT 1")
    venta = VentaDesdeDB(*consulta_venta[0])

    assert venta.id_pasajero == id_pasajero
    assert venta.id_vuelo == id_vuelo
    assert len(venta.num_reserva) == 6 and type(venta.num_reserva) == str # solo reviso que el formato sea correcto
    assert venta.precio_pagado_usd == precio_pagado_usd
    assert venta.id_estado_actual == nuevo_id_estado_actual

def test_modificar_venta_num_reserva(db_conectada: DBManager):
    ventas_manager = VentasManager(db_conectada)
    ID_STAFF = 25

    id_pasajero = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))
    id_vuelo = elegir_vuelo_valido(db_conectada, ventas_manager)
    num_reserva = "AAA123" # se genera aleatoriamente al registrarse la venta
    precio_pagado_usd = ventas_manager._obtener_precio_pagado_usd(id_vuelo)
    id_estado_actual = 3 # siempre se asigna este valor al registrar una venta

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)
    ventas_manager.registrar_venta(ID_STAFF, venta)

    consulta_id_venta: list[int] = db_conectada.consultar_columna_unica("SELECT id FROM ventas ORDER BY id DESC LIMIT 1")
    id_venta = consulta_id_venta[0]

    ventas_manager.modificar_num_reserva(ID_STAFF, id_venta)

    consulta_venta: list[FilaVenta] = db_conectada.consultar("SELECT id, num_reserva, fecha_venta, precio_pagado_usd, id_vuelo, id_estado_actual, id_pasajero FROM ventas ORDER BY id DESC LIMIT 1")
    venta = VentaDesdeDB(*consulta_venta[0])

    assert venta.id_pasajero == id_pasajero
    assert venta.id_vuelo == id_vuelo
    assert len(venta.num_reserva) == 6 and type(venta.num_reserva) == str # solo reviso que el formato sea correcto
    assert venta.precio_pagado_usd == precio_pagado_usd
    assert venta.id_estado_actual == id_estado_actual

def test_modificar_venta_id_vuelo(db_conectada: DBManager):
    ventas_manager = VentasManager(db_conectada)
    ID_STAFF = 25

    id_pasajero = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))
    id_vuelo = elegir_vuelo_valido(db_conectada, ventas_manager)
    num_reserva = "AAA123" # se genera aleatoriamente al registrarse la venta
    precio_pagado_usd = ventas_manager._obtener_precio_pagado_usd(id_vuelo)
    id_estado_actual = 3 # siempre se asigna este valor al registrar una venta

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)
    ventas_manager.registrar_venta(ID_STAFF, venta)

    consulta_id_venta: list[int] = db_conectada.consultar_columna_unica("SELECT id FROM ventas ORDER BY id DESC LIMIT 1")
    id_venta = consulta_id_venta[0]

    nuevo_id_vuelo = elegir_vuelo_valido(db_conectada, ventas_manager)
    while not id_vuelo == nuevo_id_vuelo:
        nuevo_id_vuelo = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM vuelos LIMIT 10"))

    ventas_manager.cambiar_vuelo(id_venta, ID_STAFF, nuevo_id_vuelo)

    consulta_venta: list[FilaVenta] = db_conectada.consultar("SELECT id, num_reserva, fecha_venta, precio_pagado_usd, id_vuelo, id_estado_actual, id_pasajero FROM ventas ORDER BY id DESC LIMIT 1")
    venta = VentaDesdeDB(*consulta_venta[0])

    assert venta.id_pasajero == id_pasajero
    assert venta.id_vuelo == nuevo_id_vuelo
    assert len(venta.num_reserva) == 6 and type(venta.num_reserva) == str # solo reviso que el formato sea correcto
    assert venta.precio_pagado_usd == precio_pagado_usd
    assert venta.id_estado_actual == id_estado_actual

def test_modificar_venta_id_pasajero(db_conectada: DBManager):
    ventas_manager = VentasManager(db_conectada)
    ID_STAFF = 25

    id_pasajero = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))
    id_vuelo = elegir_vuelo_valido(db_conectada, ventas_manager)
    num_reserva = "AAA123" # se genera aleatoriamente al registrarse la venta
    precio_pagado_usd = ventas_manager._obtener_precio_pagado_usd(id_vuelo)
    id_estado_actual = 3 # siempre se asigna este valor al registrar una venta

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)
    ventas_manager.registrar_venta(ID_STAFF, venta)

    consulta_id_venta: list[int] = db_conectada.consultar_columna_unica("SELECT id FROM ventas ORDER BY id DESC LIMIT 1")
    id_venta = consulta_id_venta[0]

    nuevo_id_pasajero = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))
    while not ventas_manager._verificar_pasajero(nuevo_id_pasajero) or id_pasajero == nuevo_id_pasajero:
        nuevo_id_pasajero = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))

    ventas_manager.cambiar_pasajero(id_venta, ID_STAFF, nuevo_id_pasajero)

    consulta_venta: list[FilaVenta] = db_conectada.consultar("SELECT id, num_reserva, fecha_venta, precio_pagado_usd, id_vuelo, id_estado_actual, id_pasajero FROM ventas ORDER BY id DESC LIMIT 1")
    venta = VentaDesdeDB(*consulta_venta[0])

    assert venta.id_pasajero == nuevo_id_pasajero
    assert venta.id_vuelo == id_vuelo
    assert len(venta.num_reserva) == 6 and type(venta.num_reserva) == str # solo reviso que el formato sea correcto
    assert venta.precio_pagado_usd == precio_pagado_usd
    assert venta.id_estado_actual == id_estado_actual

def test_modificar_venta_id_incorrecto(db_conectada: DBManager):
    ventas_manager = VentasManager(db_conectada)
    ID_STAFF = 25

    id_venta = 999

    nuevo_id_pasajero = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))

    with pytest.raises(Exception, match=ERROR_ID_INVALIDO):
        ventas_manager.cambiar_pasajero(id_venta, ID_STAFF, nuevo_id_pasajero)

def test_registrar_vuelo_correcto(db_conectada: DBManager):
    vuelos_manager = VuelosManager(db_conectada)
    ID_STAFF = 25

    fecha_partida_programada = datetime(2026, 1, 1)
    fecha_arribo_programada = datetime(2026, 1, 2)
    id_ruta = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM rutas LIMIT 10"))
    id_avion = elegir_avion_valido(db_conectada, id_ruta, fecha_partida_programada, fecha_arribo_programada, vuelos_manager)
    id_estado_actual = 1 # siempre se asigna este valor al registar un vuelo
    costo_operativo_usd = vuelos_manager._calcular_costo_operativo_usd(id_ruta, id_avion)
    precio_venta_usd = vuelos_manager._calcular_precio_venta_usd(costo_operativo_usd)

    vuelo = VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)
    vuelos_manager.registrar_vuelo(ID_STAFF, vuelo)

    consulta_vuelo: list[FilaVuelo] = db_conectada.consultar("SELECT id, fecha_partida_programada, fecha_arribo_programada, fecha_partida_real, fecha_arribo_real, costo_operativo_usd, precio_venta_usd, id_ruta, id_avion, id_estado_actual FROM vuelos ORDER BY id DESC LIMIT 1")
    vuelo = VueloDesdeDB(*consulta_vuelo[0])

    assert vuelo.id_ruta == id_ruta
    assert vuelo.id_avion == id_avion
    assert vuelo.id_estado_actual == id_estado_actual
    assert vuelo.fecha_partida_programada == fecha_partida_programada
    assert vuelo.fecha_arribo_programada == fecha_arribo_programada
    assert vuelo.costo_operativo_usd == costo_operativo_usd
    assert vuelo.precio_venta_usd == precio_venta_usd

def test_registrar_vuelo_fechas_incorrectas(db_conectada: DBManager):
    vuelos_manager = VuelosManager(db_conectada)
    ID_STAFF = 25

    fecha_partida_programada = datetime(2026, 1, 10)
    fecha_arribo_programada = datetime(2026, 1, 2)
    id_ruta = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM rutas LIMIT 10"))
    id_avion = elegir_avion_valido(db_conectada, id_ruta, fecha_partida_programada, fecha_arribo_programada, vuelos_manager)
    id_estado_actual = 1 # siempre se asigna este valor al registar un vuelo
    costo_operativo_usd = vuelos_manager._calcular_costo_operativo_usd(id_ruta, id_avion)
    precio_venta_usd = vuelos_manager._calcular_precio_venta_usd(costo_operativo_usd)

    vuelo = VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)

    with pytest.raises(Exception, match=ERROR_FECHAS_INVALIDAS):
        vuelos_manager.registrar_vuelo(ID_STAFF, vuelo)

def test_registrar_vuelo_avion_incorrecto(db_conectada: DBManager):
    vuelos_manager = VuelosManager(db_conectada)
    ID_STAFF = 25

    fecha_partida_programada = datetime(2026, 1, 1)
    fecha_arribo_programada = datetime(2026, 1, 2)
    id_ruta = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM rutas LIMIT 10"))

    id_aviones_disponibles = vuelos_manager._obtener_aviones_disponibles(id_ruta, fecha_arribo_programada, fecha_arribo_programada)
    id_aviones_registrados = db_conectada.consultar_columna_unica("SELECT id FROM aviones")

    for id in id_aviones_registrados:
        if id not in id_aviones_disponibles:
            id_avion = id

    id_estado_actual = 1 # siempre se asigna este valor al registar un vuelo
    costo_operativo_usd = vuelos_manager._calcular_costo_operativo_usd(id_ruta, id_avion)
    precio_venta_usd = vuelos_manager._calcular_precio_venta_usd(costo_operativo_usd)

    vuelo = VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)

    with pytest.raises(Exception, match=ERROR_AVION_Y_RUTA_INVALIDAS):
        vuelos_manager.registrar_vuelo(ID_STAFF, vuelo)

def test_modificar_vuelo_fechas(db_conectada: DBManager):
    vuelos_manager = VuelosManager(db_conectada)
    ID_STAFF = 25

    fecha_partida_programada = datetime(2026, 1, 1)
    fecha_arribo_programada = datetime(2026, 1, 2)
    id_ruta = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM rutas LIMIT 10"))
    id_avion = elegir_avion_valido(db_conectada, id_ruta, fecha_partida_programada, fecha_arribo_programada, vuelos_manager)
    id_estado_actual = 1 # siempre se asigna este valor al registar un vuelo
    costo_operativo_usd = vuelos_manager._calcular_costo_operativo_usd(id_ruta, id_avion)
    precio_venta_usd = vuelos_manager._calcular_precio_venta_usd(costo_operativo_usd)

    vuelo = VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)
    vuelos_manager.registrar_vuelo(ID_STAFF, vuelo)

    consulta_id_vuelo: list[int] = db_conectada.consultar_columna_unica("SELECT id FROM vuelos ORDER BY id DESC LIMIT 1")
    id_vuelo = consulta_id_vuelo[0]

    nueva_fecha_partida_programada = datetime(2028, 1, 10)
    nueva_fecha_arribo_programada = datetime(2028, 1, 11)

    vuelos_manager.modificar_fechas(id_vuelo, ID_STAFF, nueva_fecha_partida_programada, nueva_fecha_arribo_programada)

    consulta_vuelo: list[FilaVuelo] = db_conectada.consultar("SELECT id, fecha_partida_programada, fecha_arribo_programada, fecha_partida_real, fecha_arribo_real, costo_operativo_usd, precio_venta_usd, id_ruta, id_avion, id_estado_actual FROM vuelos ORDER BY id DESC LIMIT 1")
    vuelo = VueloDesdeDB(*consulta_vuelo[0])

    assert vuelo.fecha_partida_programada == nueva_fecha_partida_programada
    assert vuelo.fecha_arribo_programada == nueva_fecha_arribo_programada
    assert vuelo.costo_operativo_usd == costo_operativo_usd
    assert vuelo.precio_venta_usd == precio_venta_usd
    assert vuelo.id_ruta == id_ruta
    assert vuelo.id_avion == id_avion
    assert vuelo.id_estado_actual == id_estado_actual

def test_modificar_vuelo_avion(db_conectada: DBManager):
    vuelos_manager = VuelosManager(db_conectada)
    ID_STAFF = 25

    fecha_partida_programada = datetime(2026, 1, 1)
    fecha_arribo_programada = datetime(2026, 1, 2)
    id_ruta = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM rutas LIMIT 10"))
    id_avion = elegir_avion_valido(db_conectada, id_ruta, fecha_partida_programada, fecha_arribo_programada, vuelos_manager)
    id_estado_actual = 1 # siempre se asigna este valor al registar un vuelo
    costo_operativo_usd = vuelos_manager._calcular_costo_operativo_usd(id_ruta, id_avion)
    precio_venta_usd = vuelos_manager._calcular_precio_venta_usd(costo_operativo_usd)

    vuelo = VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)
    vuelos_manager.registrar_vuelo(ID_STAFF, vuelo)

    consulta_id_vuelo: list[int] = db_conectada.consultar_columna_unica("SELECT id FROM vuelos ORDER BY id DESC LIMIT 1")
    id_vuelo = consulta_id_vuelo[0]

    nuevo_id_avion = elegir_avion_valido(db_conectada, id_ruta, fecha_partida_programada, fecha_arribo_programada, vuelos_manager)

    vuelos_manager.modificar_avion(id_vuelo, ID_STAFF, nuevo_id_avion)

    consulta_vuelo: list[FilaVuelo] = db_conectada.consultar("SELECT id, fecha_partida_programada, fecha_arribo_programada, fecha_partida_real, fecha_arribo_real, costo_operativo_usd, precio_venta_usd, id_ruta, id_avion, id_estado_actual FROM vuelos ORDER BY id DESC LIMIT 1")
    vuelo = VueloDesdeDB(*consulta_vuelo[0])

    assert vuelo.fecha_partida_programada == fecha_partida_programada
    assert vuelo.fecha_arribo_programada == fecha_arribo_programada
    assert vuelo.costo_operativo_usd == costo_operativo_usd
    assert vuelo.precio_venta_usd == precio_venta_usd
    assert vuelo.id_ruta == id_ruta
    assert vuelo.id_avion == nuevo_id_avion
    assert vuelo.id_estado_actual == id_estado_actual

def test_modificar_vuelo_ruta(db_conectada: DBManager):
    vuelos_manager = VuelosManager(db_conectada)
    ID_STAFF = 25

    fecha_partida_programada = datetime(2026, 1, 1)
    fecha_arribo_programada = datetime(2026, 1, 2)
    id_ruta = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM rutas LIMIT 10"))
    id_avion = elegir_avion_valido(db_conectada, id_ruta, fecha_partida_programada, fecha_arribo_programada, vuelos_manager)
    id_estado_actual = 1 # siempre se asigna este valor al registar un vuelo
    costo_operativo_usd = vuelos_manager._calcular_costo_operativo_usd(id_ruta, id_avion)
    precio_venta_usd = vuelos_manager._calcular_precio_venta_usd(costo_operativo_usd)

    vuelo = VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)
    vuelos_manager.registrar_vuelo(ID_STAFF, vuelo)

    consulta_id_vuelo: list[int] = db_conectada.consultar_columna_unica("SELECT id FROM vuelos ORDER BY id DESC LIMIT 1")
    id_vuelo = consulta_id_vuelo[0]

    nuevo_id_ruta = elegir_ruta_valida(id_avion, id_ruta, vuelos_manager)

    vuelos_manager.modificar_ruta(id_vuelo, ID_STAFF, nuevo_id_ruta)

    consulta_vuelo: list[FilaVuelo] = db_conectada.consultar("SELECT id, fecha_partida_programada, fecha_arribo_programada, fecha_partida_real, fecha_arribo_real, costo_operativo_usd, precio_venta_usd, id_ruta, id_avion, id_estado_actual FROM vuelos ORDER BY id DESC LIMIT 1")
    vuelo = VueloDesdeDB(*consulta_vuelo[0])

    assert vuelo.fecha_partida_programada == fecha_partida_programada
    assert vuelo.fecha_arribo_programada == fecha_arribo_programada
    assert vuelo.costo_operativo_usd == costo_operativo_usd
    assert vuelo.precio_venta_usd == precio_venta_usd
    assert vuelo.id_ruta == nuevo_id_ruta
    assert vuelo.id_avion == id_avion
    assert vuelo.id_estado_actual == id_estado_actual

def test_modificar_vuelo_estado_en_vuelo(db_conectada: DBManager):
    vuelos_manager = VuelosManager(db_conectada)
    ID_STAFF = 25

    fecha_partida_programada = datetime(2026, 1, 1)
    fecha_arribo_programada = datetime(2026, 1, 2)
    id_ruta = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM rutas LIMIT 10"))
    id_avion = elegir_avion_valido(db_conectada, id_ruta, fecha_partida_programada, fecha_arribo_programada, vuelos_manager)
    id_estado_actual = 1 # siempre se asigna este valor al registar un vuelo
    costo_operativo_usd = vuelos_manager._calcular_costo_operativo_usd(id_ruta, id_avion)
    precio_venta_usd = vuelos_manager._calcular_precio_venta_usd(costo_operativo_usd)

    vuelo = VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)
    vuelos_manager.registrar_vuelo(ID_STAFF, vuelo)

    consulta_id_vuelo: list[int] = db_conectada.consultar_columna_unica("SELECT id FROM vuelos ORDER BY id DESC LIMIT 1")
    id_vuelo = consulta_id_vuelo[0]

    nuevo_id_estado_actual = 2 # en vuelo

    vuelos_manager.modificar_estado(id_vuelo, ID_STAFF, nuevo_id_estado_actual)

    consulta_vuelo: list[FilaVuelo] = db_conectada.consultar("SELECT id, fecha_partida_programada, fecha_arribo_programada, fecha_partida_real, fecha_arribo_real, costo_operativo_usd, precio_venta_usd, id_ruta, id_avion, id_estado_actual FROM vuelos ORDER BY id DESC LIMIT 1")
    vuelo = VueloDesdeDB(*consulta_vuelo[0])

    assert vuelo.fecha_partida_programada == fecha_partida_programada
    assert vuelo.fecha_arribo_programada == fecha_arribo_programada
    assert vuelo.fecha_partida_real != None 
    assert vuelo.fecha_arribo_real == None
    assert vuelo.costo_operativo_usd == costo_operativo_usd
    assert vuelo.precio_venta_usd == precio_venta_usd
    assert vuelo.id_ruta == id_ruta
    assert vuelo.id_avion == id_avion
    assert vuelo.id_estado_actual == nuevo_id_estado_actual

def test_modificar_vuelo_estado_aterrizado(db_conectada: DBManager):
    vuelos_manager = VuelosManager(db_conectada)
    ID_STAFF = 25

    fecha_partida_programada = datetime(2026, 1, 1)
    fecha_arribo_programada = datetime(2026, 1, 2)
    id_ruta = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM rutas LIMIT 10"))
    id_avion = elegir_avion_valido(db_conectada, id_ruta, fecha_partida_programada, fecha_arribo_programada, vuelos_manager)
    id_estado_actual = 1 # siempre se asigna este valor al registar un vuelo
    costo_operativo_usd = vuelos_manager._calcular_costo_operativo_usd(id_ruta, id_avion)
    precio_venta_usd = vuelos_manager._calcular_precio_venta_usd(costo_operativo_usd)

    vuelo = VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)
    vuelos_manager.registrar_vuelo(ID_STAFF, vuelo)

    consulta_id_vuelo: list[int] = db_conectada.consultar_columna_unica("SELECT id FROM vuelos ORDER BY id DESC LIMIT 1")
    id_vuelo = consulta_id_vuelo[0]

    nuevo_id_estado_actual = 2 # en vuelo

    vuelos_manager.modificar_estado(id_vuelo, ID_STAFF, nuevo_id_estado_actual) # un vuelo no puede aterrizar si primero no está en vuelo

    nuevo_id_estado_actual = 3 # aterrizado

    vuelos_manager.modificar_estado(id_vuelo, ID_STAFF, nuevo_id_estado_actual)

    consulta_vuelo: list[FilaVuelo] = db_conectada.consultar("SELECT id, fecha_partida_programada, fecha_arribo_programada, fecha_partida_real, fecha_arribo_real, costo_operativo_usd, precio_venta_usd, id_ruta, id_avion, id_estado_actual FROM vuelos ORDER BY id DESC LIMIT 1")
    vuelo = VueloDesdeDB(*consulta_vuelo[0])

    assert vuelo.fecha_partida_programada == fecha_partida_programada
    assert vuelo.fecha_arribo_programada == fecha_arribo_programada
    assert vuelo.fecha_partida_real != None 
    assert vuelo.fecha_arribo_real != None
    assert vuelo.costo_operativo_usd == costo_operativo_usd
    assert vuelo.precio_venta_usd == precio_venta_usd
    assert vuelo.id_ruta == id_ruta
    assert vuelo.id_avion == id_avion
    assert vuelo.id_estado_actual == nuevo_id_estado_actual