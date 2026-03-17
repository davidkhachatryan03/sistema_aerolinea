import pytest
from decimal import Decimal
from datetime import datetime, date
from src.entidades import *
from src.errores import ERROR_FORMATO_DATOS

def test_asignacion_vuelo_se_crea_con_formato_correcto() -> None:
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

def test_asignacion_vuelo_se_crea_con_formato_fecha_inicio_incorrecto() -> None:
    fecha_inicio = 1234
    fecha_fin = datetime(2026, 1, 11)
    id_rol = 1
    id_vuelo = 1
    id_staff = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, id_vuelo, id_staff)

def test_asignacion_vuelo_se_crea_con_formato_fecha_fin_incorrecto() -> None:
    fecha_inicio = datetime(2026, 1, 10)
    fecha_fin = 1234
    id_rol = 1
    id_vuelo = 1
    id_staff = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, id_vuelo, id_staff)

def test_asignacion_vuelo_se_crea_con_formato_id_rol_incorrecto() -> None:
    fecha_inicio = datetime(2026, 1, 10)
    fecha_fin = datetime(2026, 1, 11)
    id_rol = True
    id_vuelo = 1
    id_staff = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, id_vuelo, id_staff)

def test_asignacion_vuelo_se_crea_con_formato_id_vuelo_incorrecto() -> None:
    fecha_inicio = datetime(2026, 1, 10)
    fecha_fin = datetime(2026, 1, 11)
    id_rol = 1
    id_vuelo = True
    id_staff = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, id_vuelo, id_staff)

def test_asignacion_vuelo_se_crea_con_formado_id_staff_incorrecto() -> None:
    fecha_inicio = datetime(2026, 1, 10)
    fecha_fin = datetime(2026, 1, 11)
    id_rol = 1
    id_vuelo = 1
    id_staff = True

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        AsignacionVueloBase(fecha_inicio, fecha_fin, id_rol, id_vuelo, id_staff)

def test_avion_se_crea_con_formato_correcto() -> None:
    matricula = "AA-1234"
    marca = "Airbus"
    modelo = "A380"
    capacidad = 400
    autonomia_km = 10000
    costo_hora_vuelo = Decimal("40.000")
    id_estado_actual = 1

    avion = AvionBase(matricula, marca, modelo, capacidad, autonomia_km, costo_hora_vuelo, id_estado_actual)

    assert avion.matricula == matricula
    assert avion.marca == marca
    assert avion.modelo == modelo
    assert avion.capacidad == capacidad
    assert avion.autonomia_km == autonomia_km
    assert avion.costo_hora_vuelo == costo_hora_vuelo
    assert avion.id_estado_actual == id_estado_actual

def test_avion_se_crea_con_formato_matricula_incorrecto() -> None:
    matricula = 12345
    marca = "Airbus"
    modelo = "A380"
    capacidad = 400
    autonomia_km = 10000
    costo_hora_vuelo = Decimal("40.000")
    id_estado_actual = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        AvionBase(matricula, marca, modelo, capacidad, autonomia_km, costo_hora_vuelo, id_estado_actual)

def test_avion_se_crea_con_formato_marca_incorrecto() -> None:
    matricula = "AA-1234"
    marca = True
    modelo = "A380"
    capacidad = 400
    autonomia_km = 10000
    costo_hora_vuelo = Decimal("40.000")
    id_estado_actual = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        AvionBase(matricula, marca, modelo, capacidad, autonomia_km, costo_hora_vuelo, id_estado_actual)

def test_avion_se_crea_con_formato_modelo_incorrecto() -> None:
    matricula = "AA-1234"
    marca = "Airbus"
    modelo = True
    capacidad = 400
    autonomia_km = 10000
    costo_hora_vuelo = Decimal("40.000")
    id_estado_actual = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        AvionBase(matricula, marca, modelo, capacidad, autonomia_km, costo_hora_vuelo, id_estado_actual)

def test_avion_se_crea_con_formato_capacidad_incorrecto() -> None:
    matricula = "AA-1234"
    marca = "Airbus"
    modelo = "A380"
    capacidad = 0
    autonomia_km = 10000
    costo_hora_vuelo = Decimal("40.000")
    id_estado_actual = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        AvionBase(matricula, marca, modelo, capacidad, autonomia_km, costo_hora_vuelo, id_estado_actual)

def test_avion_se_crea_con_formato_autonomia_km_incorrecto() -> None:
    matricula = "AA-1234"
    marca = "Airbus"
    modelo = "A380"
    capacidad = 400
    autonomia_km = -10000
    costo_hora_vuelo = Decimal("40.000")
    id_estado_actual = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        AvionBase(matricula, marca, modelo, capacidad, autonomia_km, costo_hora_vuelo, id_estado_actual)

def test_avion_se_crea_con_formato_costo_hora_vuelo_incorrecto() -> None:
    matricula = "AA-1234"
    marca = "Airbus"
    modelo = "A380"
    capacidad = 400
    autonomia_km = 10000
    costo_hora_vuelo = 40000
    id_estado_actual = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        AvionBase(matricula, marca, modelo, capacidad, autonomia_km, costo_hora_vuelo, id_estado_actual)

def test_avion_se_crea_con_formato_id_estado_actual_incorrecto() -> None:
    matricula = "AA-1234"
    marca = "Airbus"
    modelo = "A380"
    capacidad = 400
    autonomia_km = 10000
    costo_hora_vuelo = Decimal("40.000")
    id_estado_actual = 0

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        AvionBase(matricula, marca, modelo, capacidad, autonomia_km, costo_hora_vuelo, id_estado_actual)

def test_certificacion_se_crea_con_formato_correcto() -> None:
    id_staff = 1
    descripcion = "licencia"
    licencia_hasta = datetime(2026, 1, 1)

    certificacion = CertificacionStaffBase(id_staff, descripcion, licencia_hasta)

    assert certificacion.id_staff == id_staff
    assert certificacion.descripcion == descripcion
    assert certificacion.licencia_hasta == licencia_hasta

def test_certificacion_se_crea_con_formato_id_staff_incorrecto() -> None:
    id_staff = True
    descripcion = "licencia"
    licencia_hasta = datetime(2026, 1, 1)

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        CertificacionStaffBase(id_staff, descripcion, licencia_hasta)

def test_certificacion_se_crea_con_formato_descripcion_incorrecto() -> None:
    id_staff = 1
    descripcion = True
    licencia_hasta = datetime(2026, 1, 1)

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        CertificacionStaffBase(id_staff, descripcion, licencia_hasta)

def test_certificacion_se_crea_con_formato_licencia_hasta_incorrecto() -> None:
    id_staff = 1
    descripcion = "licencia"
    licencia_hasta = True

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        CertificacionStaffBase(id_staff, descripcion, licencia_hasta)

def test_se_crea_documento_con_formato_correcto() -> None:
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

def test_se_crea_documento_con_formato_num_documento_incorrecto() -> None:
    num_documento = 123
    fecha_vencimiento = date(2040, 1, 1)
    pais_emision = "ARG"
    id_pasajero = 1
    id_tipo_documento = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        DocumentoBase(num_documento, fecha_vencimiento, pais_emision, id_pasajero, id_tipo_documento)

def test_se_crea_documento_con_formato_fecha_vencimiento_incorrecto() -> None:
    num_documento = "35287453"
    fecha_vencimiento = True
    pais_emision = "ARG"
    id_pasajero = 1
    id_tipo_documento = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        DocumentoBase(num_documento, fecha_vencimiento, pais_emision, id_pasajero, id_tipo_documento)

def test_se_crea_documento_con_formato_pais_emision_incorrecto() -> None:
    num_documento = "35287453"
    fecha_vencimiento = date(2040, 1, 1)
    pais_emision = True
    id_pasajero = 1
    id_tipo_documento = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        DocumentoBase(num_documento, fecha_vencimiento, pais_emision, id_pasajero, id_tipo_documento)

def test_se_crea_documento_con_formato_id_pasajero_incorrecto() -> None:
    num_documento = "35287453"
    fecha_vencimiento = date(2040, 1, 1)
    pais_emision = "ARG"
    id_pasajero = -1
    id_tipo_documento = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        DocumentoBase(num_documento, fecha_vencimiento, pais_emision, id_pasajero, id_tipo_documento)

def test_se_crea_documento_con_formato_id_tipo_documento_incorrecto() -> None:
    num_documento = "35287453"
    fecha_vencimiento = date(2040, 1, 1)
    pais_emision = "ARG"
    id_pasajero = 1
    id_tipo_documento = -1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        DocumentoBase(num_documento, fecha_vencimiento, pais_emision, id_pasajero, id_tipo_documento)

def test_pasajero_se_crea_con_formato_correcto() -> None:
    nombre_completo = "David Khachatryan"
    email = "email@test.com"
    telefono = 1143254683
    esta_en_lista_negra = False
    es_vip = True

    pasajero = PasajeroBase(nombre_completo, email, telefono, esta_en_lista_negra, es_vip)

    assert pasajero.nombre_completo == nombre_completo
    assert pasajero.email == email
    assert pasajero.telefono == telefono
    assert pasajero.esta_en_lista_negra == esta_en_lista_negra
    assert pasajero.es_vip == es_vip

def test_pasajero_se_crea_con_formato_nombre_completo_incorrecto() -> None:
    nombre_completo = True
    email = "email@test.com"
    telefono = 1143254683
    esta_en_lista_negra = False
    es_vip = True

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        PasajeroBase(nombre_completo, email, telefono, esta_en_lista_negra, es_vip)

def test_pasajero_se_crea_con_formato_email_incorrecto() -> None:
    nombre_completo = "David Khachatryan"
    email = True
    telefono = 1143254683
    esta_en_lista_negra = False
    es_vip = True

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        PasajeroBase(nombre_completo, email, telefono, esta_en_lista_negra, es_vip)

def test_pasajero_se_crea_con_formato_telefono_incorrecto() -> None:
    nombre_completo = "David Khachatryan"
    email = "email@test.com"
    telefono = True
    esta_en_lista_negra = False
    es_vip = True

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        PasajeroBase(nombre_completo, email, telefono, esta_en_lista_negra, es_vip)

def test_pasajero_se_crea_con_formato_esta_en_lista_negra_incorrecto() -> None:
    nombre_completo = "David Khachatryan"
    email = "email@test.com"
    telefono = 1143254683
    esta_en_lista_negra = 123
    es_vip = True

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        PasajeroBase(nombre_completo, email, telefono, esta_en_lista_negra, es_vip)

def test_pasajero_se_crea_con_formato_es_vip_incorrecto() -> None:
    nombre_completo = "David Khachatryan"
    email = "email@test.com"
    telefono = 1143254683
    esta_en_lista_negra = False
    es_vip = 123

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        PasajeroBase(nombre_completo, email, telefono, esta_en_lista_negra, es_vip)

def test_ruta_se_crea_con_formato_correcto() -> None:
    num_vuelo = "AA1234"
    origen = "EZE"
    destino = "CDG"
    distancia_km = 11100
    duracion_min = 780

    ruta = RutaBase(num_vuelo, origen, destino, distancia_km, duracion_min)

    assert ruta.num_vuelo == num_vuelo
    assert ruta.origen == origen
    assert ruta.destino == destino
    assert ruta.distancia_km == distancia_km
    assert ruta.duracion_min == duracion_min

def test_ruta_se_crea_con_formato_num_vuelo_incorrecto() -> None:
    num_vuelo = 1234
    origen = "EZE"
    destino = "CDG"
    distancia_km = 11100
    duracion_min = 780

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        RutaBase(num_vuelo, origen, destino, distancia_km, duracion_min)

def test_ruta_se_crea_con_formato_origen_incorrecto() -> None:
    num_vuelo = "AA1234"
    origen = "EZ"
    destino = "CDG"
    distancia_km = 11100
    duracion_min = 780

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        RutaBase(num_vuelo, origen, destino, distancia_km, duracion_min)

def test_ruta_se_crea_con_formato_destino_incorrecto() -> None:
    num_vuelo = "AA1234"
    origen = "EZE"
    destino = "CD"
    distancia_km = 11100
    duracion_min = 780

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        RutaBase(num_vuelo, origen, destino, distancia_km, duracion_min)

def test_ruta_se_crea_con_formato_distancia_km_incorrecto() -> None:
    num_vuelo = "AA1234"
    origen = "EZE"
    destino = "CDG"
    distancia_km = -11100
    duracion_min = 780

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        RutaBase(num_vuelo, origen, destino, distancia_km, duracion_min)

def test_ruta_se_crea_con_formato_duracion_min_incorrecto() -> None: 
    num_vuelo = "AA1234" 
    origen = "EZE"
    destino = "CDG"
    distancia_km = 11100
    duracion_min = -780

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        RutaBase(num_vuelo, origen, destino, distancia_km, duracion_min)

def test_se_crea_tarjeta_embarque_con_formato_correcto() -> None:
    id_estado_actual = 1
    id_venta = 1

    tarjeta_embarque = TarjetaEmbarqueBase(id_estado_actual, id_venta)

    assert tarjeta_embarque.id_estado_actual == id_estado_actual
    assert tarjeta_embarque.id_venta == id_venta

def test_se_crea_tarjeta_embarque_con_formato_id_estado_actual_incorrecto() -> None:
    id_estado_actual = -1
    id_venta = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        TarjetaEmbarqueBase(id_estado_actual, id_venta)

def test_se_crea_tarjeta_embarque_con_formato_id_venta_incorrecto() -> None:
    id_estado_actual = 1
    id_venta = -1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        TarjetaEmbarqueBase(id_estado_actual, id_venta)

def test_se_crea_venta_con_formato_correcto() -> None:
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

def test_se_crea_venta_con_formato_id_pasajero_incorrecto() -> None:
    id_pasajero = -1
    id_vuelo = 1
    num_reserva = "AAA123"
    precio_pagado_usd = Decimal("1000.32")
    id_estado_actual = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

def test_se_crea_venta_con_formato_id_vuelo_incorrecto() -> None:
    id_pasajero = 1
    id_vuelo = -1
    num_reserva = "AAA123"
    precio_pagado_usd = Decimal("1000.32")
    id_estado_actual = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

def test_se_crea_venta_con_formato_num_reserva_incorrecto() -> None:
    id_pasajero = 1
    id_vuelo = 1
    num_reserva = "AAA12345"
    precio_pagado_usd = Decimal("1000.32")
    id_estado_actual = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

def test_se_crea_venta_con_formato_precio_pagado_usd_incorrecto() -> None:
    id_pasajero = 1
    id_vuelo = 1
    num_reserva = "AAA123"
    precio_pagado_usd = 1000.32
    id_estado_actual = 1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

def test_se_crea_venta_con_formato_id_estado_actual_incorrecto() -> None:
    id_pasajero = 1
    id_vuelo = 1
    num_reserva = "AAA123"
    precio_pagado_usd = Decimal("1000.32")
    id_estado_actual = -1

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        VentaBase(id_pasajero, id_vuelo, num_reserva, precio_pagado_usd, id_estado_actual)

def test_se_crea_vuelo_con_formato_correcto() -> None:
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

def test_se_crea_vuelo_con_formato_id_ruta_incorrecto() -> None:
    id_ruta = -1
    id_avion = 1
    id_estado_actual = 1
    fecha_partida_programada = datetime(2026, 1, 1)
    fecha_arribo_programada = datetime(2026, 1, 2)
    costo_operativo_usd = Decimal("1000.10")
    precio_venta_usd = Decimal("1300.13")

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)

def test_se_crea_vuelo_con_formato_id_avion_incorrecto() -> None:
    id_ruta = 1
    id_avion = -1
    id_estado_actual = 1
    fecha_partida_programada = datetime(2026, 1, 1)
    fecha_arribo_programada = datetime(2026, 1, 2)
    costo_operativo_usd = Decimal("1000.10")
    precio_venta_usd = Decimal("1300.13")

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)

def test_se_crea_vuelo_con_formato_id_estado_actual_incorrecto() -> None:
    id_ruta = 1
    id_avion = 1
    id_estado_actual = -1
    fecha_partida_programada = datetime(2026, 1, 1)
    fecha_arribo_programada = datetime(2026, 1, 2)
    costo_operativo_usd = Decimal("1000.10")
    precio_venta_usd = Decimal("1300.13")

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)

def test_se_crea_vuelo_con_formato_fecha_partida_programada_incorrecto() -> None:
    id_ruta = 1
    id_avion = 1
    id_estado_actual = 1
    fecha_partida_programada = True
    fecha_arribo_programada = datetime(2026, 1, 2)
    costo_operativo_usd = Decimal("1000.10")
    precio_venta_usd = Decimal("1300.13")

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)

def test_se_crea_vuelo_con_formato_fecha_arribo_programada_incorrecto() -> None:
    id_ruta = 1
    id_avion = 1
    id_estado_actual = 1
    fecha_partida_programada = datetime(2026, 1, 1)
    fecha_arribo_programada = True
    costo_operativo_usd = Decimal("1000.10")
    precio_venta_usd = Decimal("1300.13")

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)

def test_se_crea_vuelo_con_formato_costo_operativo_usd_incorrecto() -> None:
    id_ruta = 1
    id_avion = 1
    id_estado_actual = 1
    fecha_partida_programada = datetime(2026, 1, 1)
    fecha_arribo_programada = datetime(2026, 1, 2)
    costo_operativo_usd = 1000.10
    precio_venta_usd = Decimal("1300.13")

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)

def test_se_crea_vuelo_con_formato_precio_venta_usd_incorrecto() -> None:
    id_ruta = 1
    id_avion = 1
    id_estado_actual = 1
    fecha_partida_programada = datetime(2026, 1, 1)
    fecha_arribo_programada = datetime(2026, 1, 2)
    costo_operativo_usd = Decimal("1000.10")
    precio_venta_usd = 1300.13

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        VueloBase(id_ruta, id_avion, id_estado_actual, fecha_partida_programada, fecha_arribo_programada, costo_operativo_usd, precio_venta_usd)