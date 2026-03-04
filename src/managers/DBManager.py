from typing import Any, cast
import os
import mysql.connector
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from dotenv import load_dotenv 

load_dotenv()

class DBManager:
    def __init__(self) -> None:
        self.host: str = os.environ["DB_HOST"]
        self.user: str = os.environ["DB_USER"]
        self.password: str = os.environ["DB_PASS"]
        self.db_name: str = os.environ["DB_NAME"]
        self.dir_sql: str = os.path.join(os.getcwd(), "sql")

    def conectar(self) -> None:
        self.conexion: MySQLConnection = cast(MySQLConnection, mysql.connector.connect(
            host = self.host,
            port = 3306,
            user = self.user,
            password = self.password,
            db = self.db_name
        ))

        if self.conexion.is_connected():
            print("Conexión establecida.\n") 
            self.cursor = self.conexion.cursor()

    def desconectar(self) -> None:
        if self.conexion and self.cursor:
            self.conexion.close()
            self.cursor.close()
            print("Conexión finalizada.")

    def obtener_cursor(self) -> MySQLCursor:
        return self.cursor
    
    def obtener_conexion(self) -> MySQLConnection:
        return self.conexion
    
    def ejecutar_archivo_sql(self, ruta_archivo: str) -> None:
        if self.cursor == None:
            raise Exception("Error: no hay cursor disponible.")
        
        with open(ruta_archivo, "r") as f:
            comandos = f.read().split(";")
            
            for comando in comandos:
                self.cursor.execute(comando)

    def consultar(self, query: str, valores: tuple | list | None = None) -> list[tuple]:
        if self.cursor == None:
            raise Exception("Error: no hay cursor disponible.")
        
        self.cursor.execute(query, valores)
        resultados: list[tuple] = cast(list[tuple], self.cursor.fetchall())

        return resultados
    
    def consultar_columna_unica(self, query: str, valores: tuple | list | None = None) -> list[Any]:
        if self.cursor == None:
            raise Exception("Error: no hay cursor disponible.")
        
        self.cursor.execute(query, valores)
        resultados: list[Any] = [elemento[0] for elemento in self.cursor.fetchall()]

        return resultados
    
    def commit(self) -> None:
        self.conexion.commit()
    
    def rollback(self) -> None:
        self.conexion.rollback()

    def execute(self, query: str, valores: tuple | list | None = None) -> None:
        self.cursor.execute(query, valores)

    def crear_db(self) -> None:
        self.ejecutar_archivo_sql(os.path.join(self.dir_sql, "crear_db.sql"))

    def borrar_db(self) -> None:
        self.execute("DROP DATABASE IF EXISTS aerolinea;")

    def borrar_datos(self) -> None:
        self.ejecutar_archivo_sql(os.path.join(self.dir_sql, "borrar_datos.sql"))