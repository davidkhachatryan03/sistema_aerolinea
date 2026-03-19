from typing import Any
from src.managers.DBManager import DBManager

class TablaManager:

    def __init__(self, tabla: str, db_manager: DBManager) -> None:
        self.db_manager: DBManager = db_manager
        self.tabla: str = tabla

    def agregar_fila(self, id_staff: int, entidad) -> None:
        if self.db_manager.obtener_cursor() == None or self.db_manager.obtener_conexion() == None:
            print("No hay cursor.")
            return
        
        self.db_manager.execute("SET @usuario = %s", (id_staff,))

        datos = entidad.to_dict()

        columnas: str = ", ".join(map(str, datos.keys()))
        valores: list[Any] = ", ".join(map(str, datos.values())).split(", ")
        cantidad_columnas: str = ", ".join(["%s"] * len(datos))

        for i in range(len(valores)):
            if valores[i] == "None":
                valores[i] = None
            elif valores[i] == "False":
                valores[i] = False
            elif valores[i] == "True":
                valores[i] = True

        query = f"""
                INSERT INTO {self.tabla} ({columnas})
                VALUES ({cantidad_columnas})
                """
        
        self.db_manager.execute(query, valores)

        if self.db_manager.obtener_cursor().rowcount == 1:
            print("Fila agregada correctamente.\n")
            self.db_manager.commit()
        else:
            print("Hubo un error.\n")
            self.db_manager.rollback()

    def modificar_fila(self, entidad, id_staff_modifica: int, campo: str, valor: Any) -> None:
        if self.db_manager.obtener_cursor() == None or self.db_manager.obtener_conexion() == None:
                print("No hay cursor.")
                return

        self.db_manager.execute("SET @usuario = %s", (id_staff_modifica,))

        query: str =    f"""
                        UPDATE {self.tabla}
                        SET {campo} = %s
                        WHERE id = %s      
                        """
        
        valores = (valor, entidad.id)
        self.db_manager.execute(query, valores)

        if self.db_manager.obtener_cursor().rowcount == 1:
            print("Fila agregada correctamente.\n")
            self.db_manager.commit()
        else:
            print("Hubo un error.\n")
            self.db_manager.rollback()

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