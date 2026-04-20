import pytest
from collections.abc import Callable
from src.managers import DBManager, VentasManager
from src.entidades import VentaBase, VentaDesdeDB, VueloBase, VueloDesdeDB, PasajeroBase, PasajeroDesdeDB
from src.columnas import COLUMNAS_VENTAS
from src.errores import ERROR_STAFF_INVALIDO, ERROR_PASAJERO_INVALIDO, ERROR_VUELO_INVALIDO, ERROR_SIN_ASIENTOS, ERROR_ESTADO_INVALIDO

def test_registrar_venta_correcta(venta_registrada: Callable[[], tuple[VentaBase, VentaDesdeDB]]) -> None:
    venta_valida_sin_registrar, ultima_venta_registrada = venta_registrada()

    assert ultima_venta_registrada.id_pasajero == venta_valida_sin_registrar.id_pasajero
    assert ultima_venta_registrada.id_vuelo == venta_valida_sin_registrar.id_vuelo
    assert ultima_venta_registrada.num_reserva != None
    assert ultima_venta_registrada.precio_pagado_usd == venta_valida_sin_registrar.precio_pagado_usd
    assert ultima_venta_registrada.id_estado_actual == venta_valida_sin_registrar.id_estado_actual

def test_registrar_venta_staff_invalido(venta_registrada: Callable[[], tuple[VentaBase, VentaDesdeDB]], ventas_manager: VentasManager) -> None:
    venta_valida_sin_registrar, ultima_venta_registrada = venta_registrada()

    ID_STAFF = 999 # cambio el id_staff por uno erróneo.

    with pytest.raises(Exception, match=ERROR_STAFF_INVALIDO):
        ventas_manager.registrar_venta(ID_STAFF, venta_valida_sin_registrar)

def test_registrar_venta_pasajero_invalido(venta_registrada: Callable[[], tuple[VentaBase, VentaDesdeDB]], ventas_manager: VentasManager, id_staff: int) -> None:
    venta_valida_sin_registrar, ultima_venta_registrada = venta_registrada()

    nuevo_id_pasajero = 999
    venta_valida_sin_registrar.id_pasajero = nuevo_id_pasajero

    with pytest.raises(Exception, match=ERROR_PASAJERO_INVALIDO):
        ventas_manager.registrar_venta(id_staff, venta_valida_sin_registrar)

def test_registrar_venta_vuelo_invalido(venta_registrada: Callable[[], tuple[VentaBase, VentaDesdeDB]], ventas_manager: VentasManager, id_staff: int) -> None:
    venta_valida_sin_registrar, ultima_venta_registrada = venta_registrada()

    nuevo_id_vuelo = 999
    venta_valida_sin_registrar.id_vuelo = nuevo_id_vuelo

    with pytest.raises(Exception, match=ERROR_VUELO_INVALIDO):
        ventas_manager.registrar_venta(id_staff, venta_valida_sin_registrar)

def test_registrar_venta_vuelo_lleno(venta_registrada: Callable[[], tuple[VentaBase, VentaDesdeDB]], ventas_manager: VentasManager, id_staff: int) -> None:
    venta_valida_sin_registrar, ultima_venta_registrada = venta_registrada()

    while ventas_manager._verificar_capacidad(ultima_venta_registrada.id_vuelo):
        ventas_manager.registrar_venta(id_staff, venta_valida_sin_registrar)

    with pytest.raises(Exception, match=ERROR_SIN_ASIENTOS):
        ventas_manager.registrar_venta(id_staff, venta_valida_sin_registrar)

def test_modificar_venta_num_reserva(db_conectada: DBManager, venta_registrada: Callable[[], tuple[VentaBase, VentaDesdeDB]], ventas_manager: VentasManager, id_staff: int) -> None:
    venta_valida_sin_registrar, ultima_venta_registrada = venta_registrada()

    ventas_manager.modificar_num_reserva(id_staff, ultima_venta_registrada) # genera un nuevo número de reserva automáticamente.

    ultima_venta_registrada_modificada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    assert ultima_venta_registrada_modificada.id_pasajero == ultima_venta_registrada.id_pasajero
    assert ultima_venta_registrada_modificada.id_vuelo == ultima_venta_registrada.id_vuelo
    assert ultima_venta_registrada_modificada.num_reserva != ultima_venta_registrada.num_reserva
    assert ultima_venta_registrada_modificada.precio_pagado_usd == ultima_venta_registrada.precio_pagado_usd
    assert ultima_venta_registrada_modificada.id_estado_actual == ultima_venta_registrada.id_estado_actual

def test_modificar_venta_estado_correcto(db_conectada: DBManager, venta_registrada: Callable[[], tuple[VentaBase, VentaDesdeDB]], ventas_manager: VentasManager, id_staff: int) -> None:
    venta_valida_sin_registrar, ultima_venta_registrada = venta_registrada()

    nuevo_id_estado_actual = 1 # Pagado.

    ventas_manager.modificar_estado(ultima_venta_registrada, id_staff, nuevo_id_estado_actual)

    ultima_venta_registrada_modificada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    assert ultima_venta_registrada_modificada.id_pasajero == ultima_venta_registrada.id_pasajero
    assert ultima_venta_registrada_modificada.id_vuelo == ultima_venta_registrada.id_vuelo
    assert ultima_venta_registrada_modificada.num_reserva != None
    assert ultima_venta_registrada_modificada.precio_pagado_usd == ultima_venta_registrada.precio_pagado_usd
    assert ultima_venta_registrada_modificada.id_estado_actual == nuevo_id_estado_actual

def test_modificar_venta_estado_invalido(venta_registrada: Callable[[], tuple[VentaBase, VentaDesdeDB]], ventas_manager: VentasManager, id_staff: int) -> None:
    venta_valida_sin_registrar, ultima_venta_registrada = venta_registrada()

    nuevo_id_estado_actual = 999 # cambio el id_estado por uno erróneo.

    with pytest.raises(Exception, match=ERROR_ESTADO_INVALIDO):
        ventas_manager.modificar_estado(ultima_venta_registrada, id_staff, nuevo_id_estado_actual)

def test_modificar_venta_vuelo_correcto(db_conectada: DBManager, venta_registrada: Callable[[], tuple[VentaBase, VentaDesdeDB]], vuelo_registrado: Callable[[], tuple[VueloBase, VueloDesdeDB]], ventas_manager: VentasManager, id_staff: int) -> None:
    venta_valida_sin_registrar, ultima_venta_registrada = venta_registrada()
    vuelo_valido_sin_registrar, ultimo_vuelo_registrado = vuelo_registrado()

    ventas_manager.cambiar_vuelo(ultima_venta_registrada, id_staff, ultimo_vuelo_registrado.id)

    ultima_venta_registrada_modificada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    assert ultima_venta_registrada_modificada.id_pasajero == ultima_venta_registrada.id_pasajero
    assert ultima_venta_registrada_modificada.id_vuelo == ultimo_vuelo_registrado.id
    assert ultima_venta_registrada_modificada.num_reserva == ultima_venta_registrada.num_reserva
    assert ultima_venta_registrada_modificada.precio_pagado_usd == ultima_venta_registrada.precio_pagado_usd
    assert ultima_venta_registrada_modificada.id_estado_actual == ultima_venta_registrada.id_estado_actual

def test_modificar_venta_vuelo_incorrecto(venta_registrada: Callable[[], tuple[VentaBase, VentaDesdeDB]], ventas_manager: VentasManager, id_staff: int) -> None:
    venta_valida_sin_registrar, ultima_venta_registrada = venta_registrada()

    nuevo_id_vuelo = 999 # cambio el id_vuelo por uno erróneo.

    with pytest.raises(Exception, match=ERROR_VUELO_INVALIDO):
        ventas_manager.cambiar_vuelo(ultima_venta_registrada, id_staff, nuevo_id_vuelo)

def test_modificar_venta_pasajero_correcto(db_conectada: DBManager, venta_registrada: Callable[[], tuple[VentaBase, VentaDesdeDB]], pasajero_registrado: Callable[[], tuple[PasajeroBase, PasajeroDesdeDB]], ventas_manager: VentasManager, id_staff: int) -> None:
    venta_valida_sin_registrar, ultima_venta_registrada = venta_registrada()
    pasajero_valido_sin_registrar, ultimo_pasajero_registrado = pasajero_registrado()

    ventas_manager.cambiar_pasajero(ultima_venta_registrada, id_staff, ultimo_pasajero_registrado.id)

    ultima_venta_registrada_modificada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    assert ultima_venta_registrada_modificada.id_pasajero == ultimo_pasajero_registrado.id
    assert ultima_venta_registrada_modificada.id_vuelo == ultima_venta_registrada.id_vuelo
    assert ultima_venta_registrada_modificada.num_reserva == ultima_venta_registrada.num_reserva
    assert ultima_venta_registrada_modificada.precio_pagado_usd == ultima_venta_registrada.precio_pagado_usd
    assert ultima_venta_registrada_modificada.id_estado_actual == ultima_venta_registrada.id_estado_actual

def test_modificar_venta_pasajero_incorrecto(venta_registrada: Callable[[], tuple[VentaBase, VentaDesdeDB]], ventas_manager: VentasManager, id_staff: int) -> None:
    venta_valida_sin_registrar, ultima_venta_registrada = venta_registrada()

    nuevo_id_pasajero = 999 # cambio el id_pasajero por uno erróneo.

    with pytest.raises(Exception, match=ERROR_PASAJERO_INVALIDO):
        ventas_manager.cambiar_pasajero(ultima_venta_registrada, id_staff, nuevo_id_pasajero)