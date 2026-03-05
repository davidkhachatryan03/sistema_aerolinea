import pytest, os, random
from init_db import main
from decimal import Decimal
from datetime import datetime, date
from src.entidades import *
from src.managers import *
from src.tipos import *

db_manager = DBManager()
ventas_manager = VentasManager(db_manager)
main()

def obtener_precio_pagado_usd(id_vuelo: int) -> Decimal:
    return round(db_manager.consultar_columna_unica("SELECT costo_operativo_usd FROM vuelos WHERE id = %s", (id_vuelo, ))[0] * Decimal("1.3"), 2)

def test_registrar_venta():
    db_manager.conectar()

    ID_STAFF = 25

    id_pasajero = random.choice(db_manager.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))
    id_vuelo = random.choice(db_manager.consultar_columna_unica("SELECT id FROM vuelos LIMIT 10"))
    num_reserva = "AAA123" #se genera aleatoriamente al registrarse la venta
    precio_pagado_usd = obtener_precio_pagado_usd(id_vuelo)
    id_estado_actual = 3 #siempre se asigna este valor al registrar una venta

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

    ventas_manager.registrar_venta(ID_STAFF, venta)

    consulta_venta: list[FilaVenta] = db_manager.consultar("SELECT * FROM ventas ORDER BY id DESC LIMIT 1")

    venta = VentaDesdeDB(*consulta_venta[0])

    db_manager.desconectar()

    assert venta.id_pasajero == id_pasajero
    assert venta.id_vuelo == id_vuelo
    assert len(venta.num_reserva) == 6 and type(venta.num_reserva) == str #solo reviso que el formato sea correcto
    assert venta.precio_pagado_usd == precio_pagado_usd
    assert venta.id_estado_actual == id_estado_actual

def test_registrar_venta_id_staff_invalido():
    db_manager.conectar()

    ID_STAFF = 999
    
    id_pasajero = random.choice(db_manager.consultar_columna_unica("SELECT id FROM pasajeros LIMIT 10"))
    id_vuelo = random.choice(db_manager.consultar_columna_unica("SELECT id FROM vuelos LIMIT 10"))
    num_reserva = "AAA123" #se genera aleatoriamente al registrarse la venta
    precio_pagado_usd = obtener_precio_pagado_usd(id_vuelo)
    id_estado_actual = 3 #siempre se asigna este valor al registrar una venta

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

    db_manager.desconectar()

    with pytest.raises(Exception, match="Error: el staff ingresado no es válido."):
        ventas_manager.registrar_venta(ID_STAFF, venta)