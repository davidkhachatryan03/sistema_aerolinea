from DBManager import DBManager
from TriggerManager import *
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from typing import Any, cast
import os

def main():
    try:
        db_manager = DBManager()
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

        conexion.commit()

    except Error as ex:
        print("Error durante la conexión: {}\n".format(ex))
        conexion.rollback()

    finally:
        db_manager.desconectar()

main()