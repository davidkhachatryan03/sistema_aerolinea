from datetime import datetime, date
from decimal import Decimal

FilaAsignacionVuelo = tuple[int, datetime, datetime, int, int, int]
FilaAvion = tuple[int, str, str, str, int, int, Decimal, int]
FilaCertificacion = tuple[int, int, str, datetime]
FilaDocumento = tuple[int, str, date, str, int, int]
FilaPasajero = tuple[int, str, str, int, bool, bool]
FilaRuta = tuple[int, str, str, str, int, int]
FilaTarjetaEmbarque = tuple[int, datetime, datetime, int, int]
FilaVenta = tuple[int, str, datetime, Decimal, int, int, int]
FilaVuelo = tuple[int, datetime, datetime, datetime, datetime, Decimal, Decimal, int, int, int]