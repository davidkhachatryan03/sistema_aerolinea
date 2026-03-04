import pytest
from decimal import Decimal
from datetime import datetime, date
from src.entidades import *
from src.managers import *

ID_STAFF = 27
db_manager = DBManager()
ventas_manager = VentasManager(db_manager)

def test_registrar_venta_correcta():
    db_manager.borrar_datos()

    id_pasajero = 1
    id_vuelo = 1
    num_reserva = "AAA123"
    precio_pagado_usd = Decimal("1000.32")
    id_estado_actual = 1

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

    ventas_manager.registrar_venta(ID_STAFF, venta)

    consulta = db_manager.consultar("SELECT * FROM ventas")