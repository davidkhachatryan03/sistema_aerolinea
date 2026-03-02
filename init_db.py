from src import DBManager, TablaManager, DocumentosManager, VuelosManager, VentasManager, AsignacionesVuelosManager, TarjetasEmbarqueManager, TriggerManager, GeneradorDatos
from src.entidades import PasajeroBase, PasajeroDesdeDB, VueloBase, VueloDesdeDB, VentaBase, VentaDesdeDB, TarjetaEmbarqueBase, DocumentoBase, RutaDesdeDB, AvionDesdeDB, AsignacionVueloBase
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from typing import cast
import os

def main() -> None:
    try:
        db_manager = DBManager()
        generador_datos = GeneradorDatos(db_manager)

        db_manager.conectar()

        conexion: MySQLConnection = cast(MySQLConnection, db_manager.obtener_conexion())

        dir_actual: str = os.getcwd()
        dir_sql: str = os.path.join(dir_actual, "sql")

        db_manager.ejecutar_archivo_sql(os.path.join(dir_sql, "crear_db.sql"))

        query = "SHOW TABLES"
        tablas: list[str] = db_manager.consultar_columna_unica(query)

        for tabla in tablas:
            if tabla not in ["historial_cambios", "sys_config"]:
                trigger_manager = TriggerManager(tabla, db_manager)
                trigger_manager.crear_trigger_after_insert()
                trigger_manager.crear_trigger_after_update()
                trigger_manager.crear_trigger_after_delete()

        dir_sql_inserts: str = os.path.join(dir_sql, "inserts")
        archivos_dir_sql_inserts: list[str] = sorted(os.listdir(dir_sql_inserts))

        for archivo in archivos_dir_sql_inserts:
            db_manager.ejecutar_archivo_sql(os.path.join(dir_sql_inserts, archivo))
        
        query = "SELECT * FROM aviones"
        consulta_aviones: list[tuple] = db_manager.consultar(query)
        aviones_desde_db: list[AvionDesdeDB] = [AvionDesdeDB(*avion) for avion in consulta_aviones]

        query = "SELECT * FROM rutas"
        consulta_rutas: list[tuple] = db_manager.consultar(query)
        rutas_desde_db: list[RutaDesdeDB] = [RutaDesdeDB(*ruta) for ruta in consulta_rutas]

        pasajeros: list[PasajeroBase] = generador_datos.generar_pasajeros(100)
        pasajeros_manager = TablaManager("pasajeros", db_manager)
        for pasajero in pasajeros:
            pasajeros_manager.agregar_fila(9, pasajero.to_dict())

        query = "SELECT * FROM pasajeros"
        consulta_pasajeros: list[tuple] = db_manager.consultar(query)
        pasajeros_desde_db: list[PasajeroDesdeDB] = [PasajeroDesdeDB(*pasajero) for pasajero in consulta_pasajeros]

        documentos: list[DocumentoBase] = generador_datos.generar_documentos(pasajeros_desde_db)
        documentos_manager = DocumentosManager(db_manager)
        for documento in documentos:
            documentos_manager.registrar_documento(9, documento)

        vuelos: list[VueloBase] = generador_datos.generar_vuelos(100, rutas_desde_db, aviones_desde_db)
        vuelos_manager = VuelosManager(db_manager)
        for vuelo in vuelos:
            vuelos_manager.registrar_vuelo(9, vuelo)

        query = "SELECT * FROM vuelos"
        consulta_vuelos: list[tuple] = db_manager.consultar(query)
        vuelos_desde_db: list[VueloDesdeDB] = [VueloDesdeDB(*vuelo) for vuelo in consulta_vuelos]

        ventas: list[VentaBase] = generador_datos.generar_ventas(200, vuelos_desde_db, pasajeros_desde_db)
        ventas_manager = VentasManager(db_manager)
        for venta in ventas:
            ventas_manager.registrar_venta(9, venta)

        query = "SELECT * FROM ventas"
        consulta_ventas: list[tuple] = db_manager.consultar(query)
        ventas_desde_db: list[VentaDesdeDB] = [VentaDesdeDB(*venta) for venta in consulta_ventas]

        tarjetas_embarque: list[TarjetaEmbarqueBase] = generador_datos.generar_tarjetas_embarque(ventas_desde_db)
        tarjetas_embarque_manager = TarjetasEmbarqueManager(db_manager)
        for tarjeta_embarque in tarjetas_embarque:
            tarjetas_embarque_manager.registrar_tarjeta_embarque(9, tarjeta_embarque)

        asignaciones_vuelos: list[AsignacionVueloBase] = generador_datos.generar_asignaciones_vuelos(vuelos_desde_db)
        asignaciones_vuelos_manager = AsignacionesVuelosManager(db_manager)
        for asignacion_vuelo in asignaciones_vuelos:
            asignaciones_vuelos_manager.agregar_fila(9, asignacion_vuelo.to_dict())

        conexion.commit()

    except Error as ex:
        print("Error durante la conexión: {}\n".format(ex))
        conexion.rollback()

    finally:
        db_manager.desconectar()

main()