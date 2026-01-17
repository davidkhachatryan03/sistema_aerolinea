from datetime import datetime

class Vuelo:
    
    def __init__(self, fecha_partida_programada: datetime, fecha_arribo_programada: datetime, id_ruta: int, id_avion: int, id: int | None = None, fecha_partida_real: datetime | None=None, fecha_arribo_real: datetime | None=None, costo_operativo_usd: float | None=None, precio_venta_usd: float | None=None, id_estado_actual: int | None=None):
        self.fecha_partida_programada = fecha_partida_programada
        self.fecha_arribo_programada = fecha_arribo_programada
        self.id_ruta = id_ruta
        self.id_avion = id_avion
        self.id = id
        self.fecha_partida_real = fecha_partida_real
        self.fecha_arribo_real = fecha_arribo_real
        self.costo_operativo_usd = costo_operativo_usd
        self.precio_venta_usd = precio_venta_usd
        self.id_estado_actual = id_estado_actual

    def to_dict(self):
        datos: dict[str, datetime | int | float | None] = {
            "fecha_partida_programada": self.fecha_partida_programada,
            "fecha_arribo_programada": self.fecha_arribo_programada,
            "id_ruta": self.id_ruta,
            "id_avion": self.id_avion,
            "id": self.id,
            "fecha_partida_real": self.fecha_partida_real,
            "fecha_arribo_real": self.fecha_arribo_real,
            "costo_operativo_usd": self.costo_operativo_usd,
            "precio_venta_usd": self.precio_venta_usd,
            "id_estado_actual": self.id_estado_actual
        }

        return datos