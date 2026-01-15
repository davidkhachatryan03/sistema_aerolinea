import os
import mysql.connector
from mysql.connector import Error
from mysql.connector.connection import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from typing import Any, cast
from dotenv import load_dotenv 

load_dotenv()

class DBManager:
    def __init__(self) -> None:
        self.host: str = os.environ["DB_HOST"]
        self.user: str = os.environ["DB_USER"]
        self.password: str = os.environ["DB_PASS"]
        self.db_name: str = os.environ["DB_NAME"]
        self.conexion: MySQLConnection | None = None
        self.cursor: MySQLCursor | None = None

    def conectar(self) -> None:
        self.conexion = cast(MySQLConnection, mysql.connector.connect(
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

    def obtener_cursor(self) -> MySQLCursor | None:
        return self.cursor
    
    def obtener_conexion(self) -> MySQLConnection | None:
        return self.conexion
    
    def ejecutar_archivo_sql(self, ruta_archivo: str) -> None:
        if self.cursor == None:
            raise Exception("Error: no hay cursor disponible.")
        
        with open(ruta_archivo, "r") as f:
            comandos = f.read().split(";")
            
            for comando in comandos:
                self.cursor.execute(comando)

    def consultar(self, query: str, valores: tuple | None = None) -> list[tuple]:
        if self.cursor == None:
            raise Exception("Error: no hay cursor disponible.")
        
        self.cursor.execute(query, valores)
        resultados: list[tuple] = cast(list[tuple], self.cursor.fetchall())

        return resultados