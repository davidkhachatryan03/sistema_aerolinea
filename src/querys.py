OBTENER_COMANDANTES =   """
                        SELECT  s.id
                        FROM    staff s
                        WHERE   s.id NOT IN (
                            SELECT  av.id_staff
                            FROM    asignaciones_vuelos av
                            JOIN    vuelos v 
                            ON      av.id_vuelo = v.id
                            WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                            AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                        )
                        AND     s.id IN (
                                SELECT  cs.id_staff
                                FROM    certificaciones_staff cs
                                WHERE   cs.licencia_hasta >= %s
                        )
                        AND     s.id_cargo_actual = 1
                        AND     s.id_estado_actual = 1;
                        """

OBTENER_COPILOTOS = """
                    SELECT  s.id
                    FROM    staff s
                    WHERE   s.id NOT IN (
                        SELECT  av.id_staff
                        FROM    asignaciones_vuelos av
                        JOIN    vuelos v 
                        ON      av.id_vuelo = v.id
                        WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                        AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                    )
                    AND     s.id IN (
                            SELECT  cs.id_staff
                            FROM    certificaciones_staff cs
                            WHERE   cs.licencia_hasta >= %s
                    )
                    AND     s.id_cargo_actual = 2
                    AND     s.id_estado_actual = 1;
                    """

OBTENER_AUXILIARES_VUELO =  """
                            SELECT  s.id
                            FROM    staff s
                            WHERE   s.id NOT IN (
                                SELECT  av.id_staff
                                FROM    asignaciones_vuelos av
                                JOIN    vuelos v 
                                ON      av.id_vuelo = v.id
                                WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                                AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                            )
                            AND     s.id IN (
                                    SELECT  cs.id_staff
                                    FROM    certificaciones_staff cs
                                    WHERE   cs.licencia_hasta >= %s
                            )
                            AND     s.id_cargo_actual = 3
                            AND     s.id_estado_actual = 1;
                            """

OBTENER_MECANICOS = """
                    SELECT  s.id
                    FROM    staff s
                    WHERE   s.id NOT IN (
                        SELECT  av.id_staff
                        FROM    asignaciones_vuelos av
                        JOIN    vuelos v 
                        ON      av.id_vuelo = v.id
                        WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                        AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                    )
                    AND     s.id IN (
                            SELECT  cs.id_staff
                            FROM    certificaciones_staff cs
                            WHERE   cs.licencia_hasta >= %s
                    )
                    AND     s.id_cargo_actual = 5
                    AND     s.id_estado_actual = 1;
                    """

OBTENER_AGENTES =   """
                    SELECT  s.id
                    FROM    staff s
                    WHERE   s.id NOT IN (
                        SELECT  av.id_staff
                        FROM    asignaciones_vuelos av
                        JOIN    vuelos v 
                        ON      av.id_vuelo = v.id
                        WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                        AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                    )
                    AND     s.id IN (
                            SELECT  cs.id_staff
                            FROM    certificaciones_staff cs
                            WHERE   cs.licencia_hasta >= %s
                    )
                    AND     s.id_cargo_actual = 7
                    AND     s.id_estado_actual = 1;
                    """

OBTENER_INSPECTORES =   """
                        SELECT  s.id
                        FROM    staff s
                        WHERE   s.id NOT IN (
                            SELECT  av.id_staff
                            FROM    asignaciones_vuelos av
                            JOIN    vuelos v 
                            ON      av.id_vuelo = v.id
                            WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                            AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                        )
                        AND     s.id IN (
                                SELECT  cs.id_staff
                                FROM    certificaciones_staff cs
                                WHERE   cs.licencia_hasta >= %s
                        )
                        AND     s.id_cargo_actual = 6
                        AND     s.id_estado_actual = 1;
                        """

OBTENER_SUPERVISORES_AGENTES =  """
                                SELECT  s.id
                                FROM    staff s
                                WHERE   s.id NOT IN (
                                    SELECT  av.id_staff
                                    FROM    asignaciones_vuelos av
                                    JOIN    vuelos v 
                                    ON      av.id_vuelo = v.id
                                    WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                                    AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                                )
                                AND     s.id IN (
                                        SELECT  cs.id_staff
                                        FROM    certificaciones_staff cs
                                        WHERE   cs.licencia_hasta >= %s
                                )
                                AND     s.id_cargo_actual = 8
                                AND     s.id_estado_actual = 1;
                                """

OBTENER_SUPERVISORES_CABINA =   """
                                SELECT  s.id
                                FROM    staff s
                                WHERE   s.id NOT IN (
                                    SELECT  av.id_staff
                                    FROM    asignaciones_vuelos av
                                    JOIN    vuelos v 
                                    ON      av.id_vuelo = v.id
                                    WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                                    AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                                )
                                AND     s.id IN (
                                        SELECT  cs.id_staff
                                        FROM    certificaciones_staff cs
                                        WHERE   cs.licencia_hasta >= %s
                                )
                                AND     s.id_cargo_actual = 4
                                AND     s.id_estado_actual = 1;
                                """

OBTENER_CERTIFICACION = """
                        SELECT  id,
                                id_staff,
                                descripcion,
                                licencia_hasta,
                        FROM    certificaciones_staff
                        WHERE   id = %s
                        """

OBTENER_DOCUMENTO = """
                    SELECT  id,
                            num_documento,
                            fecha_vencimiento,
                            pais_emision,
                            id_pasajero,
                            id_tipo_documento
                    FROM    documentos
                    WHERE   id = %s
                    """

OBTENER_ULTIMO_DOCUMENTO_REGISTRADO =   """
                                        SELECT  id,
                                                num_documento,
                                                fecha_vencimiento,
                                                pais_emision,
                                                id_pasajero,
                                                id_tipo_documento
                                        FROM    documentos
                                        ORDER BY id DESC
                                        LIMIT 1
                                        """

OBTENER_PERSONAL_AVION =    """
                            SELECT  s.id
                            FROM    staff s
                            WHERE   s.id NOT IN (
                                SELECT  av.id_staff
                                FROM    asignaciones_vuelos av
                                JOIN    vuelos v 
                                ON      av.id_vuelo = v.id
                                WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= DATE_SUB(%s, INTERVAL 2 HOUR)
                                AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                            )
                            AND     s.id IN (
                                    SELECT  cs.id_staff
                                    FROM    certificaciones_staff cs
                                    WHERE   cs.licencia_hasta >= %s
                            )
                            AND     s.id_cargo_actual = %s
                            AND     s.id_estado_actual = 1;
                            """

OBTENER_STAFF = """
                SELECT  s.id
                FROM    staff s
                WHERE   s.id NOT IN (
                    SELECT  av.id_staff
                    FROM    asignaciones_vuelos av
                    JOIN    vuelos v ON av.id_vuelo = v.id
                    WHERE   DATE_SUB(v.fecha_partida_programada, INTERVAL 2 HOUR) < %s
                    AND     v.fecha_partida_programada > DATE_SUB(%s, INTERVAL 2 HOUR)
                )
                AND     s.id IN (
                        SELECT  cs.id_staff
                        FROM    certificaciones_staff cs
                        WHERE   cs.licencia_hasta >= %s
                )
                AND     s.id_cargo_actual = %s
                AND     s.id_estado_actual = 1
                """

OBTENER_TARJETA_EMBARQUE =  """
                            SELECT  id,
                                    fecha_emision,
                                    fecha_embarque,
                                    id_estado_actual,
                                    id_venta
                            FROM    ventas
                            WHERE   id = %s
                            """

OBTENER_VENTA = """
                SELECT  id,
                        num_reserva,
                        fecha_venta,
                        precio_pagado_usd,
                        id_vuelo,
                        id_estado_actual,
                        id_pasajero
                FROM    ventas
                WHERE   id = %s
                """

OBTENER_ULTIMA_VENTA_REGISTRADA =   """
                                    SELECT  id,
                                            num_reserva,
                                            fecha_venta,
                                            precio_pagado_usd,
                                            id_vuelo,
                                            id_estado_actual,
                                            id_pasajero
                                    FROM    ventas
                                    ORDER BY id DESC
                                    LIMIT 1
                                    """

OBTENER_CAPACIDAD = """
                    SELECT  a.capacidad
                    FROM    ventas ve
                    JOIN    vuelos vu
                    ON      ve.id_vuelo = vu.id
                    JOIN    aviones a
                    ON      vu.id_avion = a.id
                    WHERE   ve.id_vuelo = %s
                    LIMIT 1
                    """

OBTENER_NUM_VENTAS =    """
                        SELECT      COUNT(id_vuelo) AS num_ventas
                        FROM        ventas
                        WHERE       id_vuelo = %s
                        GROUP BY    id_vuelo
                        """

OBTENER_AVIONES =   """
                    SELECT  a.id
                    FROM    aviones a
                    WHERE   a.id NOT IN (
                        SELECT  v.id_avion
                        FROM    vuelos v
                        WHERE   DATE_ADD(v.fecha_arribo_programada, INTERVAL 1 DAY) >= %s
                        AND     v.fecha_partida_programada <= DATE_ADD(%s, INTERVAL 1 DAY)
                    )
                    AND     a.autonomia_km > (
                            SELECT distancia_km 
                            FROM rutas 
                            WHERE id = %s
                    )
                    AND     a.id_estado_actual <> 3;
                    """

OBTENER_RUTAS = """
                SELECT  id
                FROM    rutas 
                WHERE   distancia_km < (SELECT autonomia_km FROM aviones WHERE id = %s)
                """

OBTENER_VUELO = """
                SELECT  id,
                        fecha_partida_programada,
                        fecha_arribo_programada,
                        fecha_partida_real,
                        fecha_arribo_real,
                        costo_operativo_usd,
                        precio_venta_usd,
                        id_ruta,
                        id_avion,
                        id_estado_actual
                FROM    vuelos 
                WHERE   id = %s
                """

OBTENER_ULTIMO_VUELO_REGISTRADO =   """
                                    SELECT  id, 
                                            fecha_partida_programada, 
                                            fecha_arribo_programada, 
                                            fecha_partida_real, 
                                            fecha_arribo_real, 
                                            costo_operativo_usd, 
                                            precio_venta_usd, 
                                            id_ruta, 
                                            id_avion, 
                                            id_estado_actual 
                                    FROM    vuelos 
                                    ORDER BY id DESC 
                                    LIMIT 1
                                    """

OBTENER_ULTIMO_PASAJERO_REGISTRADO =    """
                                        SELECT  id,
                                                nombre_completo,
                                                email,
                                                telefono,
                                                esta_en_lista_negra,
                                                es_vip
                                        FROM    pasajeros
                                        ORDER BY id DESC
                                        LIMIT 1
                                        """

OBTENER_TODOS_LOS_AVIONES = """
                            SELECT  id,
                                    matricula, 
                                    marca, 
                                    modelo, 
                                    capacidad, 
                                    autonomia_km, 
                                    costo_hora_vuelo, 
                                    id_estado_actual 
                            FROM    aviones
                            """

OBTENER_TODAS_LAS_RUTAS =   """
                            SELECT  id,
                                    num_vuelo,
                                    origen,
                                    destino,
                                    distancia_km,
                                    duracion_min
                            FROM    rutas
                            """