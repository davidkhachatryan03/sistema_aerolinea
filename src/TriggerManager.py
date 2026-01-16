from mysql.connector import Error
from src.DBManager import DBManager
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from typing import Any, cast

class TriggerManager:

    def __init__(self, tabla: str, db_manager: DBManager) -> None:
        self.db_manager: DBManager = db_manager
        self.tabla: str = tabla
        self.cursor: MySQLCursor | None = db_manager.obtener_cursor()
        self.conexion: MySQLConnection | None = db_manager.obtener_conexion()

    def crear_trigger_after_insert(self) -> None:
        if self.cursor == None or self.conexion == None:
                print("No hay cursor.")
                return

        self.cursor.execute(f"DROP TRIGGER IF EXISTS tr_{self.tabla}_ai")

        query: str = f"""
                CREATE TRIGGER tr_{self.tabla}_ai
                AFTER INSERT ON {self.tabla}
                FOR EACH ROW
                BEGIN
                INSERT INTO historial_cambios (tabla, operacion, id_modificado, campo, valor_anterior, valor_nuevo, fecha_cambio, id_staff)
                VALUES ('{self.tabla}', 'INSERT', NEW.id, NULL, NULL, NULL, NOW(), @usuario);
                END;
                """

        self.cursor.execute(query)

    def crear_trigger_after_update(self) -> None:
        if self.cursor == None or self.conexion == None:
                print("No hay cursor.")
                return

        columnas: list[str] | None = self._obtener_columnas()

        if columnas == None:
            return

        inserts: str = ""
        for columna in columnas:
            inserts += f"""
                        IF NOT (OLD.{columna} <=> NEW.{columna}) THEN
                            INSERT INTO historial_cambios (tabla, operacion, id_modificado, campo, valor_anterior, valor_nuevo, fecha_cambio, id_staff)
                            VALUES ('{self.tabla}', 'UPDATE', OLD.id, '{columna}', OLD.{columna}, NEW.{columna}, NOW(), @usuario);
                        END IF;
                        """

        self.cursor.execute(f"DROP TRIGGER IF EXISTS tr_{self.tabla}_au")

        query: str = f"""
                CREATE TRIGGER tr_{self.tabla}_au
                AFTER UPDATE ON {self.tabla}
                FOR EACH ROW
                BEGIN
                {inserts}
                END;
                """

        self.cursor.execute(query)

    def crear_trigger_after_delete(self) -> None:
        if self.cursor == None or self.conexion == None:
                print("No hay cursor.")
                return

        self.cursor.execute(f"DROP TRIGGER IF EXISTS tr_{self.tabla}_ad")

        query: str = f"""
                CREATE TRIGGER tr_{self.tabla}_ad
                AFTER DELETE ON {self.tabla}
                FOR EACH ROW
                BEGIN
                INSERT INTO historial_cambios (tabla, operacion, id_modificado, campo, valor_anterior, valor_nuevo, fecha_cambio, id_staff)
                VALUES ('{self.tabla}', 'DELETE', OLD.id, NULL, NULL, NULL, NOW(), @usuario);
                END;
                """
        
        self.cursor.execute(query)

    def _obtener_columnas(self) -> list[str] | None:
        if self.cursor == None or self.conexion == None:
            print("No hay cursor.")
            return
        
        query: str = f"SHOW COLUMNS FROM {self.tabla}"

        self.cursor.execute(query)

        columnas: list[tuple[str, str, str, str, str | None, str]] = cast(list[tuple[str, str, str, str, str | None, str]], self.cursor.fetchall())

        columnas_formateadas: list[str] = []
        while columnas:
            columnas_formateadas.append(columnas.pop()[0])

        columnas_formateadas.reverse()

        return columnas_formateadas