import pytest
from src.managers import *
from src.tipos import *
from src.entidades import *
from src.querys import *
from src.columnas import *
from src.errores import *
from src.GeneradorDatos import GeneradorDatos

def generar_pasajeros(generador_datos: GeneradorDatos, cant: int) -> list[PasajeroBase]:
    pasajeros: list[PasajeroBase] = generador_datos.generar_pasajeros(cant)
    return pasajeros

def generar_vuelos_validos(generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, cant: int, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB]) -> list[VueloBase]:
    vuelos_validos: list[VueloBase] = []

    while not len(vuelos_validos) == cant:
        vuelo_generado = generador_datos.generar_vuelos(1, rutas, aviones)[0]
        if vuelos_manager._verificar_avion(vuelo_generado.id_avion, vuelo_generado.id_ruta, vuelo_generado.fecha_partida_programada, vuelo_generado.fecha_arribo_programada):
            vuelos_validos.append(vuelo_generado)
    
    return vuelos_validos

def generar_ventas(generador_datos: GeneradorDatos, cant: int, pasajeros: list[PasajeroDesdeDB], vuelos: list[VueloDesdeDB]) -> list[VentaBase]:
    ventas: list[VentaBase] = generador_datos.generar_ventas(cant, vuelos, pasajeros)
    return ventas

def registrar_pasajeros(pasajeros_manager: TablaManager, pasajeros: list[PasajeroBase], id_staff: int) -> None:
    for pasajero in pasajeros:
        pasajeros_manager.agregar_fila(id_staff, pasajero)

def registrar_vuelos(vuelos_manager: VuelosManager, vuelos: list[VueloBase], id_staff: int) -> None:
    for vuelo in vuelos:
        vuelos_manager.registrar_vuelo(id_staff, vuelo)

def registrar_venta(ventas_manager: VentasManager, ventas: list[VentaBase], id_staff: int) -> None:
    for venta in ventas:
        ventas_manager.registrar_venta(id_staff, venta)

def test_registrar_tarjeta_embarque_correcta(db_conectada: DBManager, generador_datos: GeneradorDatos, tarjetas_embarque_manager: TarjetasEmbarqueManager, pasajeros_manager: TablaManager, vuelos_manager: VuelosManager, ventas_manager: VentasManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    pasajero: PasajeroBase = generar_pasajeros(generador_datos, 1)[0]
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]

    registrar_pasajeros(pasajeros_manager, [pasajero], id_staff)
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)
    
    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    venta: VentaBase = generar_ventas(generador_datos, 1, [ultimo_pasajero_registrado], [ultimo_vuelo_registrado])[0]

    registrar_venta(ventas_manager, [venta], id_staff)
    
    ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    id_estado_actual = 1 # Emitida.

    tarjeta_embarque = TarjetaEmbarqueBase(id_estado_actual, ultima_venta_registrada.id)

    tarjetas_embarque_manager.registrar_tarjeta_embarque(id_staff, tarjeta_embarque)

    ultima_tarjeta_embarque_registrada = TarjetaEmbarqueDesdeDB(*db_conectada.consultar_ultima_fila("tarjetas_embarque", COLUMNAS_TARJETAS_EMBARQUE))

    assert ultima_tarjeta_embarque_registrada.id_estado_actual == tarjeta_embarque.id_estado_actual
    assert ultima_tarjeta_embarque_registrada.id_venta == tarjeta_embarque.id_venta

def test_registrar_tarjeta_embarque_staff_invalido(db_conectada: DBManager, generador_datos: GeneradorDatos, tarjetas_embarque_manager: TarjetasEmbarqueManager, pasajeros_manager: TablaManager, vuelos_manager: VuelosManager, ventas_manager: VentasManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    pasajero: PasajeroBase = generar_pasajeros(generador_datos, 1)[0]
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]

    registrar_pasajeros(pasajeros_manager, [pasajero], id_staff)
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)
    
    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    venta: VentaBase = generar_ventas(generador_datos, 1, [ultimo_pasajero_registrado], [ultimo_vuelo_registrado])[0]

    registrar_venta(ventas_manager, [venta], id_staff)
    
    ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    id_estado_actual = 1 # Emitida.

    tarjeta_embarque = TarjetaEmbarqueBase(id_estado_actual, ultima_venta_registrada.id)

    ID_STAFF = 999 # cambio el id_staff por uno erróneo.

    with pytest.raises(Exception, match=ERROR_STAFF_INVALIDO):
        tarjetas_embarque_manager.registrar_tarjeta_embarque(ID_STAFF, tarjeta_embarque)

def test_modificar_tarjeta_embarque_estado_embarcado(db_conectada: DBManager, generador_datos: GeneradorDatos, tarjetas_embarque_manager: TarjetasEmbarqueManager, pasajeros_manager: TablaManager, vuelos_manager: VuelosManager, ventas_manager: VentasManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    pasajero: PasajeroBase = generar_pasajeros(generador_datos, 1)[0]
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]

    registrar_pasajeros(pasajeros_manager, [pasajero], id_staff)
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)
    
    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    venta: VentaBase = generar_ventas(generador_datos, 1, [ultimo_pasajero_registrado], [ultimo_vuelo_registrado])[0]
    registrar_venta(ventas_manager, [venta], id_staff)
    
    ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    id_estado_actual = 1 # Emitida.
    tarjeta_embarque = TarjetaEmbarqueBase(id_estado_actual, ultima_venta_registrada.id)
    tarjetas_embarque_manager.registrar_tarjeta_embarque(id_staff, tarjeta_embarque)

    ultima_tarjeta_embarque_registrada = TarjetaEmbarqueDesdeDB(*db_conectada.consultar_ultima_fila("tarjetas_embarque", COLUMNAS_TARJETAS_EMBARQUE))

    nuevo_id_estado_actual = 4 # Embarcado.

    tarjetas_embarque_manager.cambiar_estado(ultima_tarjeta_embarque_registrada, id_staff, nuevo_id_estado_actual)

    ultima_tarjeta_embarque_registrada = TarjetaEmbarqueDesdeDB(*db_conectada.consultar_ultima_fila("tarjetas_embarque", COLUMNAS_TARJETAS_EMBARQUE))

    assert ultima_tarjeta_embarque_registrada.id_estado_actual == nuevo_id_estado_actual
    assert ultima_tarjeta_embarque_registrada.id_venta == tarjeta_embarque.id_venta
    assert ultima_tarjeta_embarque_registrada.fecha_embarque != None

def test_modificar_tarjeta_embarque_estado_invalido(db_conectada: DBManager, generador_datos: GeneradorDatos, tarjetas_embarque_manager: TarjetasEmbarqueManager, pasajeros_manager: TablaManager, vuelos_manager: VuelosManager, ventas_manager: VentasManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB], id_staff: int) -> None:
    pasajero: PasajeroBase = generar_pasajeros(generador_datos, 1)[0]
    vuelo: VueloBase = generar_vuelos_validos(generador_datos, vuelos_manager, 1, rutas, aviones)[0]

    registrar_pasajeros(pasajeros_manager, [pasajero], id_staff)
    registrar_vuelos(vuelos_manager, [vuelo], id_staff)
    
    ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))
    ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

    venta: VentaBase = generar_ventas(generador_datos, 1, [ultimo_pasajero_registrado], [ultimo_vuelo_registrado])[0]

    registrar_venta(ventas_manager, [venta], id_staff)
    
    ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

    id_estado_actual = 1 # Emitida.

    tarjeta_embarque = TarjetaEmbarqueBase(id_estado_actual, ultima_venta_registrada.id)

    tarjetas_embarque_manager.registrar_tarjeta_embarque(id_staff, tarjeta_embarque)

    ultima_tarjeta_embarque_registrada = TarjetaEmbarqueDesdeDB(*db_conectada.consultar_ultima_fila("tarjetas_embarque", COLUMNAS_TARJETAS_EMBARQUE))

    nuevo_id_estado_actual = 999 # cambio el id_estado_actual por uno erróneo.

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        tarjetas_embarque_manager.cambiar_estado(ultima_tarjeta_embarque_registrada, id_staff, nuevo_id_estado_actual)