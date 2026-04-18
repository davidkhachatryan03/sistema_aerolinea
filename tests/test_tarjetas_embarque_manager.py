import pytest
from collections.abc import Callable
from src.managers import *
from src.tipos import *
from src.entidades import *
from src.querys import *
from src.columnas import *
from src.errores import *

def test_registrar_tarjeta_embarque_correcta(tarjeta_embarque_registrada: Callable[[], tuple[TarjetaEmbarqueBase, TarjetaEmbarqueDesdeDB]]) -> None:
    tarjeta_embarque_valida_sin_registrar, ultima_tarjeta_embarque_registrada = tarjeta_embarque_registrada()

    assert ultima_tarjeta_embarque_registrada.fecha_emision != None
    assert ultima_tarjeta_embarque_registrada.fecha_embarque == None
    assert ultima_tarjeta_embarque_registrada.id_estado_actual == tarjeta_embarque_valida_sin_registrar.id_estado_actual
    assert ultima_tarjeta_embarque_registrada.id_venta == tarjeta_embarque_valida_sin_registrar.id_venta

def test_registrar_tarjeta_embarque_staff_invalido(tarjeta_embarque_registrada: Callable[[], tuple[TarjetaEmbarqueBase, TarjetaEmbarqueDesdeDB]], tarjetas_embarque_manager: TarjetasEmbarqueManager) -> None:
    tarjeta_embarque_valida_sin_registrar, ultima_tarjeta_embarque_registrada = tarjeta_embarque_registrada()

    ID_STAFF = 999 # cambio el id_staff por uno erróneo.

    with pytest.raises(Exception, match=ERROR_STAFF_INVALIDO):
        tarjetas_embarque_manager.registrar_tarjeta_embarque(ID_STAFF, tarjeta_embarque_valida_sin_registrar)

def test_modificar_tarjeta_embarque_estado_embarcado(db_conectada: DBManager, tarjeta_embarque_registrada: Callable[[], tuple[TarjetaEmbarqueBase, TarjetaEmbarqueDesdeDB]], tarjetas_embarque_manager: TarjetasEmbarqueManager, id_staff: int) -> None:
    tarjeta_embarque_valida_sin_registrar, ultima_tarjeta_embarque_registrada = tarjeta_embarque_registrada()

    nuevo_id_estado_actual = 4 # Embarcado.

    tarjetas_embarque_manager.cambiar_estado(ultima_tarjeta_embarque_registrada, id_staff, nuevo_id_estado_actual)

    ultima_tarjeta_embarque_registrada = TarjetaEmbarqueDesdeDB(*db_conectada.consultar_ultima_fila("tarjetas_embarque", COLUMNAS_TARJETAS_EMBARQUE))

    assert ultima_tarjeta_embarque_registrada.fecha_emision != None
    assert ultima_tarjeta_embarque_registrada.fecha_embarque != None
    assert ultima_tarjeta_embarque_registrada.id_estado_actual == nuevo_id_estado_actual
    assert ultima_tarjeta_embarque_registrada.id_venta == tarjeta_embarque_valida_sin_registrar.id_venta

def test_modificar_tarjeta_embarque_estado_invalido(tarjeta_embarque_registrada: Callable[[], tuple[TarjetaEmbarqueBase, TarjetaEmbarqueDesdeDB]], tarjetas_embarque_manager: TarjetasEmbarqueManager, id_staff: int) -> None:
    tarjeta_embarque_valida_sin_registrar, ultima_tarjeta_embarque_registrada = tarjeta_embarque_registrada()

    nuevo_id_estado_actual = 999 # cambio el id_estado_actual por uno erróneo.

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        tarjetas_embarque_manager.cambiar_estado(ultima_tarjeta_embarque_registrada, id_staff, nuevo_id_estado_actual)