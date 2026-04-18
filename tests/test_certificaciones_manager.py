import pytest, random
from collections.abc import Callable
from datetime import datetime
from src.managers import *
from src.tipos import *
from src.entidades import *
from src.querys import *
from src.columnas import *
from src.errores import *

def test_registrar_certificacion_correcta(certificacion_registrada: Callable[[], tuple[CertificacionStaffBase, CertificacionStaffDesdeDB]]) -> None:
    certificacion_valida_sin_registrar, ultima_certificacion_registrada = certificacion_registrada()

    assert ultima_certificacion_registrada.id_staff == certificacion_valida_sin_registrar.id_staff
    assert ultima_certificacion_registrada.descripcion == certificacion_valida_sin_registrar.descripcion
    assert ultima_certificacion_registrada.licencia_hasta == certificacion_valida_sin_registrar.licencia_hasta

def test_registrar_certificacion_staff_invalido(certificacion_registrada: Callable[[], tuple[CertificacionStaffBase, CertificacionStaffDesdeDB]], certificaciones_manager: CertificacionesStaffManager) -> None:
    certificacion_valida_sin_registrar, ultima_certificacion_registrada = certificacion_registrada()

    ID_STAFF = 999 # cambio el id_staff por uno erróneo.

    with pytest.raises(Exception, match=ERROR_STAFF_INVALIDO):
        certificaciones_manager.registrar_certificacion(ID_STAFF, certificacion_valida_sin_registrar)

def test_modificar_certificacion_staff_correcto(db_conectada: DBManager, certificacion_registrada: Callable[[], tuple[CertificacionStaffBase, CertificacionStaffDesdeDB]], certificaciones_manager: CertificacionesStaffManager, staff: list[StaffDesdeDB], id_staff: int) -> None:
    certificacion_valida_sin_registrar, ultima_certificacion_registrada = certificacion_registrada()

    nuevo_id_staff = random.choice(staff).id
    while nuevo_id_staff == ultima_certificacion_registrada.id:
        nuevo_id_staff = random.choice(staff).id

    certificaciones_manager.modificar_id_staff(ultima_certificacion_registrada, id_staff, nuevo_id_staff)

    ultima_certificacion_registrada_modificada = CertificacionStaffDesdeDB(*db_conectada.consultar_ultima_fila("certificaciones_staff", COLUMNAS_CERTIFICACIONES_STAFF))

    assert ultima_certificacion_registrada_modificada.id_staff == nuevo_id_staff
    assert ultima_certificacion_registrada_modificada.descripcion == ultima_certificacion_registrada.descripcion
    assert ultima_certificacion_registrada_modificada.licencia_hasta == ultima_certificacion_registrada.licencia_hasta

def test_modificar_certificacion_staff_invalido(certificacion_registrada: Callable[[], tuple[CertificacionStaffBase, CertificacionStaffDesdeDB]], certificaciones_manager: CertificacionesStaffManager, staff: list[StaffDesdeDB]) -> None:
    certificacion_valida_sin_registrar, ultima_certificacion_registrada = certificacion_registrada()

    nuevo_id_staff = random.choice(staff).id
    while nuevo_id_staff == ultima_certificacion_registrada.id:
        nuevo_id_staff = random.choice(staff).id

    ID_STAFF = 999

    with pytest.raises(Exception, match=ERROR_STAFF_INVALIDO):
        certificaciones_manager.modificar_id_staff(ultima_certificacion_registrada, ID_STAFF, nuevo_id_staff)

def test_modificar_certificacion_descripcion_correcta(db_conectada: DBManager, certificacion_registrada: Callable[[], tuple[CertificacionStaffBase, CertificacionStaffDesdeDB]], certificaciones_manager: CertificacionesStaffManager, id_staff: int) -> None:
    certificacion_valida_sin_registrar, ultima_certificacion_registrada = certificacion_registrada()

    nueva_descripcion = "Licencia profesional X"
    certificaciones_manager.modificar_descripcion(ultima_certificacion_registrada, id_staff, nueva_descripcion)

    ultima_certificacion_registrada_modificada = CertificacionStaffDesdeDB(*db_conectada.consultar_ultima_fila("certificaciones_staff", COLUMNAS_CERTIFICACIONES_STAFF))

    assert ultima_certificacion_registrada_modificada.id_staff == ultima_certificacion_registrada.id_staff
    assert ultima_certificacion_registrada_modificada.descripcion == nueva_descripcion
    assert ultima_certificacion_registrada_modificada.licencia_hasta == ultima_certificacion_registrada.licencia_hasta

def test_modificar_certificacion_descripcion_invalida(certificacion_registrada: Callable[[], tuple[CertificacionStaffBase, CertificacionStaffDesdeDB]], certificaciones_manager: CertificacionesStaffManager, id_staff: int) -> None:
    certificacion_valida_sin_registrar, ultima_certificacion_registrada = certificacion_registrada()

    nueva_descripcion = 123

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        certificaciones_manager.modificar_descripcion(ultima_certificacion_registrada, id_staff, nueva_descripcion)
    
def test_modificar_certificacion_vencimiento_correcto(db_conectada: DBManager, certificacion_registrada: Callable[[], tuple[CertificacionStaffBase, CertificacionStaffDesdeDB]], certificaciones_manager: CertificacionesStaffManager, id_staff: int) -> None:
    certificacion_valida_sin_registrar, ultima_certificacion_registrada = certificacion_registrada()

    nueva_licencia_hasta = datetime(2090, 1, 1)
    certificaciones_manager.modificar_vencimiento(ultima_certificacion_registrada, id_staff, nueva_licencia_hasta)

    ultima_certificacion_registrada_modificada = CertificacionStaffDesdeDB(*db_conectada.consultar_ultima_fila("certificaciones_staff", COLUMNAS_CERTIFICACIONES_STAFF))

    assert ultima_certificacion_registrada_modificada.id_staff == ultima_certificacion_registrada.id_staff
    assert ultima_certificacion_registrada_modificada.descripcion == ultima_certificacion_registrada.descripcion
    assert ultima_certificacion_registrada_modificada.licencia_hasta == nueva_licencia_hasta

def test_modificar_certificacion_vencimiento_invalida(certificacion_registrada: Callable[[], tuple[CertificacionStaffBase, CertificacionStaffDesdeDB]], certificaciones_manager: CertificacionesStaffManager, id_staff: int) -> None: 
    certificacion_valida_sin_registrar, ultima_certificacion_registrada = certificacion_registrada()

    nueva_licencia_hasta = "ABC"

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        certificaciones_manager.modificar_vencimiento(ultima_certificacion_registrada, id_staff, nueva_licencia_hasta)