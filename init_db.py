from DBManager import DBManager
from TriggerManager import *
from mysql.connector import Error
import os

def main():
    try:
        db_manager = DBManager()

        cursor, conexion = db_manager.conectar()

        dir_actual = os.getcwd()
        dir_sql = os.path.join(dir_actual, "sql")

        db_manager.ejecutar_archivo_sql(os.path.join(dir_sql, "crear_db.sql"))

        cursor.execute("SHOW TABLES")

        tablas = cursor.fetchall()

        for tabla in tablas:
            if tabla[0] not in ["historial_cambios", "sys_config"]:
                trigger_manager = TriggerManager(tabla[0], db_manager)
                trigger_manager.crear_trigger_after_insert()
                trigger_manager.crear_trigger_after_update()
                trigger_manager.crear_trigger_after_delete()

        dir_sql_inserts = os.path.join(dir_sql, "inserts")
        archivos_dir_sql_inserts = sorted(os.listdir(dir_sql_inserts))

        for archivo in archivos_dir_sql_inserts:
            db_manager.ejecutar_archivo_sql(os.path.join(dir_sql_inserts, archivo))

        conexion.commit()

    except Error as ex:
        print("Error durante la conexión: {}\n".format(ex))
        conexion.rollback()

    finally:
        db_manager.desconectar()

main()