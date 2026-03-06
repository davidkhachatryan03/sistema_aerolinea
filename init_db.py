from src.GeneradorDatos import GeneradorDatos
from src.entidades import PasajeroBase, PasajeroDesdeDB, VueloBase, VueloDesdeDB, VentaBase, VentaDesdeDB, TarjetaEmbarqueBase, DocumentoBase, RutaDesdeDB, AvionDesdeDB, AsignacionVueloBase
from src.managers import AsignacionesVuelosManager, DBManager, DocumentosManager, TablaManager, TarjetasEmbarqueManager, TriggerManager, VentasManager, VuelosManager
from mysql.connector import Error
import os

def main() -> None:

    db_manager = DBManager()

    try:
        generador_datos = GeneradorDatos(db_manager)

        db_manager.conectar()

        dir_actual: str = os.getcwd()
        dir_sql: str = os.path.join(dir_actual, "sql")

        db_manager.ejecutar_archivo_sql(os.path.join(dir_sql, "crear_db.sql"))

        db_manager.execute("USE aerolinea")

        tablas: list[str] = _obtener_tablas(db_manager)

        _crear_triggers(db_manager, tablas)

        dir_sql_inserts: str = os.path.join(dir_sql, "inserts")
        archivos_dir_sql_inserts: list[str] = sorted(os.listdir(dir_sql_inserts))

        for archivo in archivos_dir_sql_inserts:
            db_manager.ejecutar_archivo_sql(os.path.join(dir_sql_inserts, archivo))
        
        aviones_desde_db: list[AvionDesdeDB] = _obtener_aviones(db_manager)
        
        rutas_desde_db: list[RutaDesdeDB] = _obtener_rutas(db_manager)

        pasajeros: list[PasajeroBase] = generador_datos.generar_pasajeros(100)
        _poblar_pasajeros(db_manager, pasajeros)

        pasajeros_desde_db: list[PasajeroDesdeDB] = _obtener_pasajeros(db_manager)

        documentos: list[DocumentoBase] = generador_datos.generar_documentos(pasajeros_desde_db)
        _poblar_documentos(db_manager, documentos)

        vuelos: list[VueloBase] = generador_datos.generar_vuelos(100, rutas_desde_db, aviones_desde_db)
        _poblar_vuelos(db_manager, vuelos)

        vuelos_desde_db: list[VueloDesdeDB] = _obtener_vuelos(db_manager)

        ventas: list[VentaBase] = generador_datos.generar_ventas(200, vuelos_desde_db, pasajeros_desde_db)
        _poblar_ventas(db_manager, ventas)

        ventas_desde_db: list[VentaDesdeDB] = _obtener_ventas(db_manager)

        tarjetas_embarque: list[TarjetaEmbarqueBase] = generador_datos.generar_tarjetas_embarque(ventas_desde_db)
        _poblar_tarjetas_embarque(db_manager, tarjetas_embarque)

        asignaciones_vuelos: list[AsignacionVueloBase] = generador_datos.generar_asignaciones_vuelos(vuelos_desde_db)
        _poblar_asignaciones_vuelos(db_manager, asignaciones_vuelos)

        db_manager.commit()

    except Error as ex:
        print("Error durante la conexión: {}\n".format(ex))
        db_manager.rollback()

    finally:
        db_manager.desconectar()

def _obtener_tablas(db_manager: DBManager) -> list[str]:
    query = "SHOW TABLES"
    tablas: list[str] = db_manager.consultar_columna_unica(query)

    return tablas

def _crear_triggers(db_manager: DBManager, tablas: list[str]) -> None:
    for tabla in tablas:
        if tabla not in ["historial_cambios", "sys_config"]:
            trigger_manager = TriggerManager(tabla, db_manager)
            trigger_manager.crear_trigger_after_insert()
            trigger_manager.crear_trigger_after_update()
            trigger_manager.crear_trigger_after_delete()

def _obtener_aviones(db_manager: DBManager) -> list[AvionDesdeDB]:
    query = "SELECT * FROM aviones"
    consulta_aviones: list[tuple] = db_manager.consultar(query)
    aviones_desde_db: list[AvionDesdeDB] = [AvionDesdeDB(*avion) for avion in consulta_aviones]

    return aviones_desde_db

def _obtener_rutas(db_manager: DBManager) -> list[RutaDesdeDB]:
    query = "SELECT * FROM rutas"
    consulta_rutas: list[tuple] = db_manager.consultar(query)
    rutas_desde_db: list[RutaDesdeDB] = [RutaDesdeDB(*ruta) for ruta in consulta_rutas]

    return rutas_desde_db

def _obtener_pasajeros(db_manager: DBManager) -> list[PasajeroDesdeDB]:
    query = "SELECT * FROM pasajeros"
    consulta_pasajeros: list[tuple] = db_manager.consultar(query)
    
    pasajeros_desde_db: list[PasajeroDesdeDB] = []
    for pasajero in consulta_pasajeros:
        pasajeros_desde_db.append(PasajeroDesdeDB(
            id=pasajero[0],
            nombre_completo=pasajero[1],
            email=pasajero[2],
            telefono=pasajero[3],
            esta_en_lista_negra=bool(pasajero[4]),
            es_vip=bool(pasajero[5])
        ))

    return pasajeros_desde_db

def _obtener_vuelos(db_manager: DBManager) -> list[VueloDesdeDB]:
    query = "SELECT * FROM vuelos"
    consulta_vuelos: list[tuple] = db_manager.consultar(query)
    vuelos_desde_db: list[VueloDesdeDB] = [VueloDesdeDB(*vuelo) for vuelo in consulta_vuelos]

    return vuelos_desde_db

def _obtener_ventas(db_manager: DBManager) -> list[VentaDesdeDB]:
    query = "SELECT * FROM ventas"
    consulta_ventas: list[tuple] = db_manager.consultar(query)
    ventas_desde_db: list[VentaDesdeDB] = [VentaDesdeDB(*venta) for venta in consulta_ventas]

    return ventas_desde_db

def _poblar_pasajeros(db_manager: DBManager, pasajeros: list[PasajeroBase]) -> None:
    pasajeros_manager = TablaManager("pasajeros", db_manager)
    for pasajero in pasajeros:
        pasajeros_manager.agregar_fila(9, pasajero.to_dict())

def _poblar_documentos(db_manager: DBManager, documentos: list[DocumentoBase]) -> None:
    documentos_manager = DocumentosManager(db_manager)
    for documento in documentos:
        documentos_manager.registrar_documento(9, documento)

def _poblar_vuelos(db_manager: DBManager, vuelos: list[VueloBase]) -> None:
    vuelos_manager = VuelosManager(db_manager)
    
    for vuelo in vuelos:
        try:
            vuelos_manager.registrar_vuelo(9, vuelo)
        except Exception:
            continue

def _poblar_ventas(db_manager: DBManager, ventas: list[VentaBase]) -> None:
    ventas_manager = VentasManager(db_manager)

    for venta in ventas:
        try:
            ventas_manager.registrar_venta(9, venta)
        except Exception:
            continue 

def _poblar_tarjetas_embarque(db_manager: DBManager, tarjetas_embarque: list[TarjetaEmbarqueBase]) -> None:
    tarjetas_embarque_manager = TarjetasEmbarqueManager(db_manager)
    for tarjeta_embarque in tarjetas_embarque:
        tarjetas_embarque_manager.registrar_tarjeta_embarque(9, tarjeta_embarque)

def _poblar_asignaciones_vuelos(db_manager: DBManager, asignaciones_vuelos: list[AsignacionVueloBase]) -> None:
    asignaciones_vuelos_manager = AsignacionesVuelosManager(db_manager)
    for asignacion_vuelo in asignaciones_vuelos:
        asignaciones_vuelos_manager.agregar_fila(9, asignacion_vuelo.to_dict())

main()