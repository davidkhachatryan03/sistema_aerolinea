from mysql.connector import Error
from DBManager import DBManager
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from typing import Any

class TablaManager:

    def __init__(self, tabla: str, db_manager: DBManager) -> None:
        self.db_manager: DBManager = db_manager
        self.tabla: str = tabla
        self.cursor: MySQLCursor | None = db_manager.obtener_cursor()
        self.conexion: MySQLConnection | None = db_manager.obtener_conexion()

    def agregar_fila(self, id_staff: int, datos: dict[str, Any]) -> None:
        if self.cursor == None or self.conexion == None:
                print("No hay cursor.")
                return
        
        self.cursor.execute("SET @usuario = %s", (id_staff,))

        columnas: str = ", ".join(map(str, datos.keys()))
        valores: list[Any] = ", ".join(map(str, datos.values())).split(", ")
        cantidad_columnas: str = ", ".join(["%s"] * len(datos))

        for i in range(len(valores)):
            if valores[i] == "None":
                valores[i] = None

        query = f"""
                INSERT INTO {self.tabla} ({columnas})
                VALUES ({cantidad_columnas})
                """
        
        self.cursor.execute(query, valores)

        if self.cursor.rowcount == 1:
            print("Fila agregada correctamente.\n")
            self.conexion.commit()
        else:
            print("Hubo un error.\n")
            self.conexion.rollback()

    def modificar_fila(self, id: int, id_staff: int, **datos) -> None:
        if self.cursor == None or self.conexion == None:
                print("No hay cursor.")
                return

        self.cursor.execute("SET @usuario = %s", (id_staff,))

        columnas: str = ", ".join(map(str, datos.keys()))
        valores: list[Any] = ", ".join(map(str, datos.values())).split(", ")

        if len(datos) == 1:
            query: str = f"""
                    UPDATE {self.tabla}
                    SET {columnas} = %s
                    WHERE id = %s      
                    """
            
            valores_: list[Any] = valores.copy()
            valores_.append(id)

            self.cursor.execute(query, valores_)

            if self.cursor.rowcount == 1:
                print("Fila agregada correctamente.\n")
                self.conexion.commit()
            else:
                print("Hubo un error.\n")
                self.conexion.rollback()

        else:
            # optimizar esto con .executemany
            for i in range(len(datos)):
                columnas_lista: list[str] = columnas.split(", ")
                query = f"""
                        UPDATE {self.tabla}
                        SET {columnas_lista[i]} = %s
                        WHERE id = %s
                        """

                valores__: tuple[Any, int] = (valores[i], id)

                self.cursor.execute(query, valores__)

                if self.cursor.rowcount == 1:
                    print("Fila agregada correctamente.\n")
                    self.conexion.commit()
                else:
                    print("Hubo un error.\n")
                    self.conexion.rollback()

    def _verificar_id_a_modificar(self, id: int) -> bool:
        query = f"SELECT 1 FROM {self.tabla} WHERE id = %s LIMIT 1"
        consulta: list[tuple] = self.db_manager.consultar(query, (id,))

        if consulta:
            return True
        
        return False

    def _verificar_id_staff(self, id: int):
        query = f"SELECT 1 FROM staff WHERE id = %s LIMIT 1"
        consulta: list[tuple] = self.db_manager.consultar(query, (id,))

        if consulta:
            return True
        
        return False