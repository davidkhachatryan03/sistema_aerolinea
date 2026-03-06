import pytest, os, random
from init_db import main
from decimal import Decimal
from datetime import datetime, date
from src.entidades import *
from src.managers import *
from src.tipos import *

main()

@pytest.fixture
def db_conectada():
    db_manager = DBManager()
    db_manager.conectar()
    db_manager.execute("USE aerolinea")
    yield db_manager
    db_manager.desconectar()

def test_registrar_venta_correcta(db_conectada: DBManager):
        ventas_manager = VentasManager(db_conectada)
        ID_STAFF = 25

        id_pasajero = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))
        id_vuelo = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM vuelos LIMIT 10"))
        num_reserva = "AAA123" # se genera aleatoriamente al registrarse la venta
        precio_pagado_usd = ventas_manager._obtener_precio_pagado_usd(id_vuelo)
        id_estado_actual = 3 # siempre se asigna este valor al registrar una venta

        venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)
        ventas_manager.registrar_venta(ID_STAFF, venta)

        consulta_venta: list[FilaVenta] = db_conectada.consultar("SELECT id, num_reserva, fecha_venta, precio_pagado_usd, id_vuelo, id_estado_actual, id_pasajero FROM ventas ORDER BY id DESC LIMIT 1")
        venta = VentaDesdeDB(*consulta_venta[0])

        assert venta.id_pasajero == id_pasajero
        assert venta.id_vuelo == id_vuelo
        assert len(venta.num_reserva) == 6 and type(venta.num_reserva) == str #solo reviso que el formato sea correcto
        assert venta.precio_pagado_usd == precio_pagado_usd
        assert venta.id_estado_actual == id_estado_actual
    
def test_registrar_venta_id_staff_invalido(db_conectada: DBManager):
    ventas_manager = VentasManager(db_conectada)
    ID_STAFF = 999
    
    id_pasajero = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))
    id_vuelo = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM vuelos LIMIT 10"))
    num_reserva = "AAA123" # se genera aleatoriamente al registrarse la venta
    precio_pagado_usd = ventas_manager._obtener_precio_pagado_usd(id_vuelo)
    id_estado_actual = 3 # siempre se asigna este valor al registrar una venta

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

    with pytest.raises(Exception, match="Error: el staff ingresado no es válido."):
        ventas_manager.registrar_venta(ID_STAFF, venta)
    
def test_registrar_venta_pasajero_invalido(db_conectada: DBManager):
    ventas_manager = VentasManager(db_conectada)
    ID_STAFF = 25

    id_pasajero = 999
    id_vuelo = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM vuelos LIMIT 10"))
    num_reserva = "AAA123" # se genera aleatoriamente al registrarse la venta
    precio_pagado_usd = ventas_manager._obtener_precio_pagado_usd(id_vuelo)
    id_estado_actual = 3 # siempre se asigna este valor al registrar una venta

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

    with pytest.raises(Exception, match="Error: el pasajero no se encuentra registrado."):
        ventas_manager.registrar_venta(ID_STAFF, venta)

def test_registrar_venta_vuelo_invalido(db_conectada: DBManager):
    ventas_manager = VentasManager(db_conectada)
    ID_STAFF = 25

    id_pasajero = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))
    id_vuelo = 999
    num_reserva = "AAA123" # se genera aleatoriamente al registrarse la venta
    precio_pagado_usd = Decimal("1000.21") # invento un precio aleatorio para que no falle la búsqueda según id_vuelo
    id_estado_actual = 3 # siempre se asigna este valor al registrar una venta

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

    with pytest.raises(Exception, match="Error: el vuelo no se encuentra registrado."):
        ventas_manager.registrar_venta(ID_STAFF, venta)

def test_registrar_venta_vuelo_lleno(db_conectada: DBManager):
    ventas_manager = VentasManager(db_conectada)
    ID_STAFF = 25
    
    id_pasajero = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))
    id_vuelo = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM vuelos LIMIT 10"))
    num_reserva = "AAA123" # se genera aleatoriamente al registrarse la venta
    precio_pagado_usd = ventas_manager._obtener_precio_pagado_usd(id_vuelo)
    id_estado_actual = 3 # siempre se asigna este valor al registrar una venta

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

    while ventas_manager._verificar_capacidad(id_vuelo):
        ventas_manager.registrar_venta(ID_STAFF, venta)

    with pytest.raises(Exception, match="Error: no hay más asientos disponibles."):
        ventas_manager.registrar_venta(ID_STAFF, venta)

def test_modificar_venta_id_estado_actual(db_conectada: DBManager):
    ventas_manager = VentasManager(db_conectada)
    ID_STAFF = 25

    id_pasajero = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))
    id_vuelo = random.choice(db_conectada.consultar_columna_unica("SELECT id FROM vuelos LIMIT 10"))
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
    assert len(venta.num_reserva) == 6 and type(venta.num_reserva) == str #solo reviso que el formato sea correcto
    assert venta.precio_pagado_usd == precio_pagado_usd
    assert venta.id_estado_actual == nuevo_id_estado_actual