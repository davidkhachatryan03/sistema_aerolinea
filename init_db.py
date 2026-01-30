from src.DBManager import DBManager
from src.TablaManager import TablaManager
from src.DocumentosManager import DocumentosManager
from src.VuelosManager import VuelosManager
from src.VentasManager import VentasManager
from src.AsignacionesVuelosManager import AsignacionesVuelosManager
from src.TarjetasEmbarqueManager import TarjetasEmbarqueManager
from src.TriggerManager import TriggerManager
from src.GeneradorDatos import GeneradorDatos
from src.entidades.Pasajero import PasajeroBase, PasajeroDesdeDB
from src.entidades.Vuelo import VueloBase, VueloDesdeDB
from src.entidades.Venta import VentaBase, VentaDesdeDB
from src.entidades.TarjetaEmbarque import TarjetaEmbarqueBase, TarjetaEmbarqueDesdeDB
from src.entidades.Documento import DocumentoBase, DocumentoDesdeDB
from src.entidades.Ruta import RutaBase, RutaDesdeDB
from src.entidades.Avion import AvionBase, AvionDesdeDB
from src.entidades.AsignacionVuelo import AsignacionVueloBase, AsignacionVueloDesdeDB
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from typing import Any, cast
import os

def main() -> None:
    try:
        db_manager = DBManager()
        generador_datos = GeneradorDatos(db_manager)

        db_manager.conectar()

        cursor: MySQLCursor | None = cast(MySQLCursor, db_manager.obtener_cursor())
        conexion: MySQLConnection | None = cast(MySQLConnection, db_manager.obtener_conexion())

        dir_actual: str = os.getcwd()
        dir_sql: str = os.path.join(dir_actual, "sql")

        db_manager.ejecutar_archivo_sql(os.path.join(dir_sql, "crear_db.sql"))

        cursor.execute("SHOW TABLES")

        tablas: list[tuple] = cursor.fetchall()

        for tabla in tablas:
            if tabla[0] not in ["historial_cambios", "sys_config"]:
                trigger_manager = TriggerManager(tabla[0], db_manager)
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
            pasajeros_manager.agregar_fila(99, pasajero.to_dict())

        query = "SELECT * FROM pasajeros"
        consulta_pasajeros: list[tuple] = db_manager.consultar(query)
        pasajeros_desde_db: list[PasajeroDesdeDB] = [PasajeroDesdeDB(*pasajero) for pasajero in consulta_pasajeros]

        documentos: list[DocumentoBase] = generador_datos.generar_documentos(pasajeros_desde_db)
        documentos_manager = DocumentosManager(db_manager)
        for documento in documentos:
            documentos_manager.registrar_documento(99, documento)

        vuelos: list[VueloBase] = generador_datos.generar_vuelos(100, rutas_desde_db, aviones_desde_db)
        vuelos_manager = VuelosManager(db_manager)
        for vuelo in vuelos:
            vuelos_manager.registrar_vuelo(99, vuelo)

        query = "SELECT * FROM vuelos"
        consulta_vuelos: list[tuple] = db_manager.consultar(query)
        vuelos_desde_db: list[VueloDesdeDB] = [VueloDesdeDB(*vuelo) for vuelo in consulta_vuelos]

        ventas: list[VentaBase] = generador_datos.generar_ventas(200, vuelos_desde_db, pasajeros_desde_db)
        ventas_manager = VentasManager(db_manager)
        for venta in ventas:
            ventas_manager.registrar_venta(99, venta)

        query = "SELECT * FROM ventas"
        consulta_ventas: list[tuple] = db_manager.consultar(query)
        ventas_desde_db: list[VentaDesdeDB] = [VentaDesdeDB(*venta) for venta in consulta_ventas]

        tarjetas_embarque: list[TarjetaEmbarqueBase] = generador_datos.generar_tarjetas_embarque(ventas_desde_db)
        tarjetas_embarque_manager = TarjetasEmbarqueManager(db_manager)
        for tarjeta_embarque in tarjetas_embarque:
            tarjetas_embarque_manager.registrar_tarjeta_embarque(99, tarjeta_embarque)

        asignaciones_vuelos: list[AsignacionVueloBase] = generador_datos.generar_asignaciones_vuelos(vuelos_desde_db)
        asignaciones_vuelos_manager = AsignacionesVuelosManager(db_manager)
        for asignacion_vuelo in asignaciones_vuelos:
            asignaciones_vuelos_manager.agregar_fila(99, asignacion_vuelo.to_dict())

        conexion.commit()

    except Error as ex:
        print("Error durante la conexión: {}\n".format(ex))
        conexion.rollback()

    finally:
        db_manager.desconectar()

main()