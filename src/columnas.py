COLUMNAS_ASIGNACIONES_VUELOS = "id, fecha_inicio, fecha_fin, id_rol, id_vuelo, id_staff"

COLUMNAS_AVIONES = "id, matricula, marca, modelo, capacidad, autonomia_km, costo_hora_vuelo, id_estado_actual"

COLUMNAS_CARGOS = "id, descripcion"

COLUMNAS_CERTIFICACIONES_STAFF = "id, id_staff, descripcion, licencia_hasta"

COLUMNAS_DOCUMENTOS = "id, num_documento, fecha_vencimiento, pais_emision, id_pasajero, id_tipo_documento"

COLUMNAS_ESTADOS_AVIONES = "id, descripcion"

COLUMNAS_ESTADOS_STAFF = "id, descripcion"

COLUMNAS_ESTADOS_TARJETAS_EMBARQUE = "id, descripcion"

COLUMNAS_ESTADOS_VENTAS = "id, descripcion"

COLUMNAS_ESTADOS_VUELOS = "id, descripcion"

COLUMNAS_HISTORIAL_CAMBIOS = "id, tabla, id_modificado, campo, valor_anterior, valor_nuevo, fecha_cambio, id_staff"

COLUMNAS_PASAJEROS = "id, nombre_completo, email, telefono, esta_en_lista_negra, es_vip"

COLUMNAS_ROLES = "id, descripcion"

COLUMNAS_RUTAS = "id, num_vuelo, origen, destino, distancia_km, duracion_min"

COLUMNAS_STAFF = "id, descripcion"

COLUMNAS_TARJETAS_EMBARQUE = "id, fecha_emision, fecha_embarque, id_estado_actual, id_venta"

COLUMNAS_TIPOS_DOCUMENTO = "id, tipo_documento"

COLUMNAS_VENTAS = "id, num_reserva, fecha_venta, precio_pagado_usd, id_vuelo, id_estado_actual, id_pasajero"

COLUMNAS_VUELOS = "id, fecha_partida_programada, fecha_arribo_programada, fecha_partida_real, fecha_arribo_real, costo_operativo_usd, precio_venta_usd, id_ruta, id_avion, id_estado_actual"