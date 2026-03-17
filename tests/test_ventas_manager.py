import pytest
from src.managers import *
from src.tipos import *
from src.entidades import *
from src.querys import *
from src.columnas import *
from src.errores import *
from src.GeneradorDatos import GeneradorDatos

def registrar_pasajeros(generador_datos: GeneradorDatos, pasajeros_manager: TablaManager, cant: int, id_staff: int) -> None:
    pasajeros_generados = generador_datos.generar_pasajeros(cant)
    for pasajero in pasajeros_generados:
        pasajeros_manager.agregar_fila(id_staff, pasajero.to_dict())

def registrar_vuelos(generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, cant: int, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    vuelos_validos: list[VueloBase] = []

    while not len(vuelos_validos) == cant:
        vuelo_generado = generador_datos.generar_vuelos(1, rutas, aviones)[0]
        if vuelos_manager._verificar_avion(vuelo_generado.id_avion, vuelo_generado.id_ruta, vuelo_generado.fecha_partida_programada, vuelo_generado.fecha_arribo_programada):
            vuelos_validos.append(vuelo_generado)

    for vuelo in vuelos_validos:
        vuelos_manager.registrar_vuelo(id_staff, vuelo)

def test_registrar_venta_correcta(db_conectada: DBManager, generador_datos: GeneradorDatos, ventas_manager: VentasManager, pasajeros_manager: TablaManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)
    registrar_vuelos(generador_datos, vuelos_manager, 1, rutas, aviones, id_staff)

    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    id_pasajero = ultimo_pasajero_registrado.id
    id_vuelo = ultimo_vuelo_registrado.id
    num_reserva = "AAA123" # se genera aleatoriamente por el manager al registrarse la venta.
    precio_pagado_usd = ultimo_vuelo_registrado.precio_venta_usd
    id_estado_actual = 3 # Reservado. Se asigna automáticamente por el manager al registrarse la venta.

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)
    ventas_manager.registrar_venta(id_staff, venta)

    ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    assert ultima_venta_registrada.id_pasajero == id_pasajero
    assert ultima_venta_registrada.id_vuelo == id_vuelo
    assert ultima_venta_registrada.precio_pagado_usd == precio_pagado_usd
    assert ultima_venta_registrada.id_estado_actual == id_estado_actual

def test_registrar_venta_id_staff_invalido(db_conectada: DBManager, generador_datos: GeneradorDatos, ventas_manager: VentasManager, pasajeros_manager: TablaManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)
    registrar_vuelos(generador_datos, vuelos_manager, 1, rutas, aviones, id_staff)

    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    id_pasajero = ultimo_pasajero_registrado.id
    id_vuelo = ultimo_vuelo_registrado.id
    num_reserva = "AAA123" # se genera aleatoriamente por el manager al registrarse la venta.
    precio_pagado_usd = ultimo_vuelo_registrado.precio_venta_usd
    id_estado_actual = 3 # Reservado. Se asigna automáticamente por el manager al registrarse la venta.

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

    ID_STAFF = 999 # cambio el id_staff por uno erróneo.

    with pytest.raises(Exception, match=ERROR_STAFF_INVALIDO):
        ventas_manager.registrar_venta(ID_STAFF, venta)

def test_registrar_venta_pasajero_invalido(db_conectada: DBManager, generador_datos: GeneradorDatos, ventas_manager: VentasManager, pasajeros_manager: TablaManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)
    registrar_vuelos(generador_datos, vuelos_manager, 1, rutas, aviones, id_staff)

    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    id_pasajero = 999
    id_vuelo = ultimo_vuelo_registrado.id
    num_reserva = "AAA123" # se genera aleatoriamente por el manager al registrarse la venta.
    precio_pagado_usd = ultimo_vuelo_registrado.precio_venta_usd
    id_estado_actual = 3 # Reservado. Se asigna automáticamente por el manager al registrarse la venta.

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

    with pytest.raises(Exception, match=ERROR_PASAJERO_INVALIDO):
        ventas_manager.registrar_venta(id_staff, venta)

def test_registrar_venta_vuelo_invalido(db_conectada: DBManager, generador_datos: GeneradorDatos, ventas_manager: VentasManager, pasajeros_manager: TablaManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)
    registrar_vuelos(generador_datos, vuelos_manager, 1, rutas, aviones, id_staff)

    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    id_pasajero = ultimo_pasajero_registrado.id
    id_vuelo = 999
    num_reserva = "AAA123" # se genera aleatoriamente por el manager al registrarse la venta.
    precio_pagado_usd = ultimo_vuelo_registrado.precio_venta_usd
    id_estado_actual = 3 # Reservado. Se asigna automáticamente por el manager al registrarse la venta.

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

    with pytest.raises(Exception, match=ERROR_VUELO_INVALIDO):
        ventas_manager.registrar_venta(id_staff, venta)

def test_registrar_venta_vuelo_lleno(db_conectada: DBManager, generador_datos: GeneradorDatos, ventas_manager: VentasManager, pasajeros_manager: TablaManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)
    registrar_vuelos(generador_datos, vuelos_manager, 1, rutas, aviones, id_staff)

    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    id_pasajero = ultimo_pasajero_registrado.id
    id_vuelo = ultimo_vuelo_registrado.id
    num_reserva = "AAA123" # se genera aleatoriamente por el manager al registrarse la venta.
    precio_pagado_usd = ultimo_vuelo_registrado.precio_venta_usd
    id_estado_actual = 3 # Reservado. Se asigna automáticamente por el manager al registrarse la venta.

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

    while ventas_manager._verificar_capacidad(id_vuelo):
        ventas_manager.registrar_venta(id_staff, venta)

    with pytest.raises(Exception, match=ERROR_SIN_ASIENTOS):
        ventas_manager.registrar_venta(id_staff, venta)

def test_modificar_venta_id_estado_actual_correcto(db_conectada: DBManager, generador_datos: GeneradorDatos, ventas_manager: VentasManager, pasajeros_manager: TablaManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)
    registrar_vuelos(generador_datos, vuelos_manager, 1, rutas, aviones, id_staff)

    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    id_pasajero = ultimo_pasajero_registrado.id
    id_vuelo = ultimo_vuelo_registrado.id
    num_reserva = "AAA123" # se genera aleatoriamente por el manager al registrarse la venta.
    precio_pagado_usd = ultimo_vuelo_registrado.precio_venta_usd
    id_estado_actual = 3 # Reservado. Se asigna automáticamente por el manager al registrarse la venta.

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)
    ventas_manager.registrar_venta(id_staff, venta)

    nuevo_id_estado_actual = 1 # Pagado.

    ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    ventas_manager.modificar_estado(ultima_venta_registrada.id, id_staff, nuevo_id_estado_actual)

    ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    assert ultima_venta_registrada.id_pasajero == id_pasajero
    assert ultima_venta_registrada.id_vuelo == id_vuelo
    assert ultima_venta_registrada.precio_pagado_usd == precio_pagado_usd
    assert ultima_venta_registrada.id_estado_actual == nuevo_id_estado_actual

def test_modificar_venta_id_estado_actual_invalido(db_conectada: DBManager, generador_datos: GeneradorDatos, ventas_manager: VentasManager, pasajeros_manager: TablaManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)
    registrar_vuelos(generador_datos, vuelos_manager, 1, rutas, aviones, id_staff)

    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    id_pasajero = ultimo_pasajero_registrado.id
    id_vuelo = ultimo_vuelo_registrado.id
    num_reserva = "AAA123" # se genera aleatoriamente por el manager al registrarse la venta.
    precio_pagado_usd = ultimo_vuelo_registrado.precio_venta_usd
    id_estado_actual = 3 # Reservado. Se asigna automáticamente por el manager al registrarse la venta.

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)
    ventas_manager.registrar_venta(id_staff, venta)

    nuevo_id_estado_actual = 999

    ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    with pytest.raises(Exception, match=ERROR_ESTADO_INVALIDO):
        ventas_manager.modificar_estado(ultima_venta_registrada.id, id_staff, nuevo_id_estado_actual)

def test_modificar_venta_num_reserva(db_conectada: DBManager, generador_datos: GeneradorDatos, ventas_manager: VentasManager, pasajeros_manager: TablaManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)
    registrar_vuelos(generador_datos, vuelos_manager, 1, rutas, aviones, id_staff)

    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    id_pasajero = ultimo_pasajero_registrado.id
    id_vuelo = ultimo_vuelo_registrado.id
    num_reserva = "AAA123" # se genera aleatoriamente por el manager al registrarse la venta.
    precio_pagado_usd = ultimo_vuelo_registrado.precio_venta_usd
    id_estado_actual = 3 # Reservado. Se asigna automáticamente por el manager al registrarse la venta.

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)
    ventas_manager.registrar_venta(id_staff, venta)

    ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    ventas_manager.modificar_num_reserva(id_staff, ultima_venta_registrada.id) # genera un nuevo número de reserva automáticamente.

    ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    assert ultima_venta_registrada.id_pasajero == id_pasajero
    assert ultima_venta_registrada.id_vuelo == id_vuelo
    assert ultima_venta_registrada.num_reserva != num_reserva
    assert ultima_venta_registrada.precio_pagado_usd == precio_pagado_usd
    assert ultima_venta_registrada.id_estado_actual == id_estado_actual

def test_modificar_venta_id_vuelo_correcto(db_conectada: DBManager, generador_datos: GeneradorDatos, ventas_manager: VentasManager, pasajeros_manager: TablaManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)
    registrar_vuelos(generador_datos, vuelos_manager, 1, rutas, aviones, id_staff)

    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    id_pasajero = ultimo_pasajero_registrado.id
    id_vuelo = ultimo_vuelo_registrado.id
    num_reserva = "AAA123" # se genera aleatoriamente por el manager al registrarse la venta.
    precio_pagado_usd = ultimo_vuelo_registrado.precio_venta_usd
    id_estado_actual = 3 # Reservado. Se asigna automáticamente por el manager al registrarse la venta.

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)
    ventas_manager.registrar_venta(id_staff, venta)

    ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    registrar_vuelos(generador_datos, vuelos_manager, 1, rutas, aviones, id_staff)

    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))
    nuevo_id_vuelo = ultimo_vuelo_registrado.id
    ventas_manager.cambiar_vuelo(ultima_venta_registrada.id, id_staff, nuevo_id_vuelo)

    ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    assert ultima_venta_registrada.id_pasajero == id_pasajero
    assert ultima_venta_registrada.id_vuelo == nuevo_id_vuelo
    assert ultima_venta_registrada.precio_pagado_usd == precio_pagado_usd
    assert ultima_venta_registrada.id_estado_actual == id_estado_actual

def test_modificar_venta_id_vuelo_incorrecto(db_conectada: DBManager, generador_datos: GeneradorDatos, ventas_manager: VentasManager, pasajeros_manager: TablaManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)
    registrar_vuelos(generador_datos, vuelos_manager, 1, rutas, aviones, id_staff)

    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    id_pasajero = ultimo_pasajero_registrado.id
    id_vuelo = ultimo_vuelo_registrado.id
    num_reserva = "AAA123" # se genera aleatoriamente por el manager al registrarse la venta.
    precio_pagado_usd = ultimo_vuelo_registrado.precio_venta_usd
    id_estado_actual = 3 # Reservado. Se asigna automáticamente por el manager al registrarse la venta.

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)
    ventas_manager.registrar_venta(id_staff, venta)

    ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    nuevo_id_vuelo = 999

    with pytest.raises(Exception, match=ERROR_VUELO_INVALIDO):
        ventas_manager.cambiar_vuelo(ultima_venta_registrada.id, id_staff, nuevo_id_vuelo)

def test_modificar_venta_id_pasajero_correcto(db_conectada: DBManager, generador_datos: GeneradorDatos, ventas_manager: VentasManager, pasajeros_manager: TablaManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)
    registrar_vuelos(generador_datos, vuelos_manager, 1, rutas, aviones, id_staff)

    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    id_pasajero = ultimo_pasajero_registrado.id
    id_vuelo = ultimo_vuelo_registrado.id
    num_reserva = "AAA123" # se genera aleatoriamente por el manager al registrarse la venta.
    precio_pagado_usd = ultimo_vuelo_registrado.precio_venta_usd
    id_estado_actual = 3 # Reservado. Se asigna automáticamente por el manager al registrarse la venta.

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)
    ventas_manager.registrar_venta(id_staff, venta)

    ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)

    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    nuevo_id_pasajero = ultimo_pasajero_registrado.id
    ventas_manager.cambiar_pasajero(ultima_venta_registrada.id, id_staff, nuevo_id_pasajero)

    ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    assert ultima_venta_registrada.id_pasajero == nuevo_id_pasajero
    assert ultima_venta_registrada.id_vuelo == id_vuelo
    assert ultima_venta_registrada.precio_pagado_usd == precio_pagado_usd
    assert ultima_venta_registrada.id_estado_actual == id_estado_actual

def test_modificar_venta_id_pasajero_incorrecto(db_conectada: DBManager, generador_datos: GeneradorDatos, ventas_manager: VentasManager, pasajeros_manager: TablaManager, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)
    registrar_vuelos(generador_datos, vuelos_manager, 1, rutas, aviones, id_staff)

    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    id_pasajero = ultimo_pasajero_registrado.id
    id_vuelo = ultimo_vuelo_registrado.id
    num_reserva = "AAA123" # se genera aleatoriamente por el manager al registrarse la venta.
    precio_pagado_usd = ultimo_vuelo_registrado.precio_venta_usd
    id_estado_actual = 3 # Reservado. Se asigna automáticamente por el manager al registrarse la venta.

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)
    ventas_manager.registrar_venta(id_staff, venta)

    ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    nuevo_id_pasajero = 999

    with pytest.raises(Exception, match=ERROR_PASAJERO_INVALIDO):
        ventas_manager.cambiar_pasajero(ultima_venta_registrada.id, id_staff, nuevo_id_pasajero)