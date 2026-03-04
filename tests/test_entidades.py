import pytest
from decimal import Decimal
from datetime import datetime, date
from src.entidades import *

def test_pasajero_se_crea_con_formato_correcto():
    nombre_completo = "David Khachatryan"
    email = "email@test.com"
    telefono = "1143254683"
    esta_en_lista_negra = False
    es_vip = True

    pasajero = PasajeroBase(nombre_completo, email, telefono, esta_en_lista_negra, es_vip)

    assert pasajero.nombre_completo == nombre_completo
    assert pasajero.email == email
    assert pasajero.telefono == telefono
    assert pasajero.esta_en_lista_negra == esta_en_lista_negra
    assert pasajero.es_vip == es_vip

def test_pasajero_se_crea_con_formato_incorrecto():
    nombre_completo = True
    email = 3
    telefono = 23
    esta_en_lista_negra = 1
    es_vip = 2

    with pytest.raises(Exception):
        PasajeroBase(nombre_completo, email, telefono, esta_en_lista_negra, es_vip)

def test_asignacion_vuelo_se_crea_con_formato_correcto():
    fecha_inicio = datetime(2026, 1, 10)
    fecha_fin = datetime(2026, 1, 11)
    id_rol = 1
    id_vuelo = 1
    id_staff = 1

    asignacion_vuelo = AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, id_vuelo, id_staff)

    assert asignacion_vuelo.fecha_inicio == fecha_inicio
    assert asignacion_vuelo.fecha_fin == fecha_fin
    assert asignacion_vuelo.id_rol == id_rol
    assert asignacion_vuelo.id_vuelo == id_vuelo
    assert asignacion_vuelo.id_staff == id_staff

def test_asignacion_vuelo_se_crea_con_formato_incorrecto():
    fecha_inicio = "a"
    fecha_fin = "a"
    id_rol = "a" 
    id_vuelo = "a"
    id_staff = "a"

    with pytest.raises(Exception):
        AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, id_vuelo, id_staff)

def test_certificacion_se_crea_con_formato_correcto():
    id_staff = 1
    descripcion = "licencia"
    licencia_hasta = datetime(2026, 1, 1)

    certificacion = CertificacionStaffBase(id_staff, descripcion, licencia_hasta)

    assert certificacion.id_staff == id_staff
    assert certificacion.descripcion == descripcion
    assert certificacion.licencia_hasta == licencia_hasta

def test_certificacion_se_crea_con_formato_incorrecto():
    id_staff = 1
    descripcion = 1
    licencia_hasta = 1

    with pytest.raises(Exception):
        CertificacionStaffBase(id_staff, descripcion, licencia_hasta)

def test_se_crea_documento_con_formato_correcto():
    num_documento = "35287453"
    fecha_vencimiento = date(2040, 1, 1)
    pais_emision = "ARG"
    id_pasajero = 1
    id_tipo_documento = 1

    documento = DocumentoBase(num_documento, fecha_vencimiento, pais_emision, id_pasajero, id_tipo_documento)

    assert documento.num_documento == num_documento
    assert documento.fecha_vencimiento == fecha_vencimiento
    assert documento.pais_emision == pais_emision
    assert documento.id_pasajero == id_pasajero
    assert documento.id_tipo_documento == id_tipo_documento

def test_se_crea_documento_con_formato_incorrecto():
    num_documento = 1
    fecha_vencimiento = 1
    pais_emision = 1
    id_pasajero = 1
    id_tipo_documento = 1

    with pytest.raises(Exception):
        DocumentoBase(num_documento, fecha_vencimiento, pais_emision, id_pasajero, id_tipo_documento)

def test_se_crea_tarjeta_embarque_con_formato_correcto():
    id_estado_actual = 1
    id_venta = 1

    tarjeta_embarque = TarjetaEmbarqueBase(id_estado_actual, id_venta)

    assert tarjeta_embarque.id_estado_actual == id_estado_actual
    assert tarjeta_embarque.id_venta == id_venta

def test_se_crea_tarjeta_embarque_con_formato_incorrecto():
    id_estado_actual = "a"
    id_venta = "a"

    with pytest.raises(Exception):
        TarjetaEmbarqueBase(id_estado_actual, id_venta)

def test_se_crea_venta_con_formato_correcto():
    id_pasajero = 1
    id_vuelo = 1
    num_reserva = "AAA123"
    precio_pagado_usd = Decimal("1000.32")
    id_estado_actual = 1

    venta = VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

    assert venta.id_pasajero == id_pasajero
    assert venta.id_vuelo == id_vuelo
    assert venta.num_reserva == num_reserva
    assert venta.precio_pagado_usd == precio_pagado_usd
    assert venta.id_estado_actual == id_estado_actual

def test_se_crea_venta_con_formato_incorrecto():
    id_pasajero = 1
    id_vuelo = 1
    num_reserva = 1
    precio_pagado_usd = 1
    id_estado_actual = 1

    with pytest.raises(Exception):
        VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

def test_se_crea_vuelo_con_fomato_correcto():
    id_ruta = 1
    id_avion = 1
    id_estado_actual = 1
    fecha_partida_programada = datetime(2026, 1, 1)
    fecha_arribo_programada = datetime(2026, 1, 2)
    costo_operativo_usd = Decimal("1000.10")
    precio_venta_usd = Decimal("1300.13")

    vuelo = VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)

    assert vuelo.id_ruta == id_ruta
    assert vuelo.id_avion == id_avion
    assert vuelo.id_estado_actual == id_estado_actual
    assert vuelo.fecha_partida_programada == fecha_partida_programada
    assert vuelo.fecha_arribo_programada == fecha_arribo_programada
    assert vuelo.costo_operativo_usd == costo_operativo_usd
    assert vuelo.precio_venta_usd == precio_venta_usd

def test_se_crea_vuelo_con_formato_incorrecto():
    id_ruta = 1
    id_avion = 1
    id_estado_actual = 1
    fecha_partida_programada = 1
    fecha_arribo_programada = 1
    costo_operativo_usd = 1
    precio_venta_usd = 1

    with pytest.raises(Exception):
        VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)