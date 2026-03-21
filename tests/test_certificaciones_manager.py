import pytest, random
from datetime import datetime
from src.managers import *
from src.tipos import *
from src.entidades import *
from src.querys import *
from src.columnas import *
from src.errores import *
from src.GeneradorDatos import GeneradorDatos

def registrar_certificaciones(certificaciones_manager: CertificacionesStaffManager, certificaciones: list[CertificacionStaffBase], id_staff: int) -> None:
    for certificado in certificaciones:
        certificaciones_manager.registrar_certificacion(id_staff, certificado)

def generar_certificaciones(cant: int, staff: list[StaffDesdeDB]) -> list[CertificacionStaffBase]:
    certificaciones: list[CertificacionStaffBase] = []

    for _ in range(cant):
        id_staff: int = random.choice(staff).id
        descripcion = "Licencia X"
        licencia_hasta = datetime(2060, 1, 1)

        certificacion = CertificacionStaffBase(id_staff, descripcion, licencia_hasta)
        certificaciones.append(certificacion)

    return certificaciones

def test_registrar_certificacion_correcta(db_conectada: DBManager, certificaciones_manager: CertificacionesStaffManager, staff: list[StaffDesdeDB], id_staff: int) -> None:
    certificacion: CertificacionStaffBase = generar_certificaciones(1, staff)[0]

    certificaciones_manager.registrar_certificacion(id_staff, certificacion)
    ultima_certificacion_registrada = CertificacionStaffDesdeDB(*db_conectada.consultar_ultima_fila("certificaciones_staff", COLUMNAS_CERTIFICACIONES_STAFF))

    assert ultima_certificacion_registrada.id_staff == certificacion.id_staff
    assert ultima_certificacion_registrada.descripcion == certificacion.descripcion
    assert ultima_certificacion_registrada.licencia_hasta == certificacion.licencia_hasta

def test_registrar_certificacion_staff_invalido(certificaciones_manager: CertificacionesStaffManager, staff: list[StaffDesdeDB]) -> None:
    certificacion: CertificacionStaffBase = generar_certificaciones(1, staff)[0]

    ID_STAFF = 999

    with pytest.raises(Exception, match=ERROR_STAFF_INVALIDO):
        certificaciones_manager.registrar_certificacion(ID_STAFF, certificacion)

def test_modificar_certificacion_staff_correcto(db_conectada: DBManager, certificaciones_manager: CertificacionesStaffManager, staff: list[StaffDesdeDB], id_staff: int) -> None:
    certificacion: CertificacionStaffBase = generar_certificaciones(1, staff)[0]

    certificaciones_manager.registrar_certificacion(id_staff, certificacion)
    ultima_certificacion_registrada = CertificacionStaffDesdeDB(*db_conectada.consultar_ultima_fila("certificaciones_staff", COLUMNAS_CERTIFICACIONES_STAFF))

    nuevo_id_staff = random.choice(staff).id
    while nuevo_id_staff == ultima_certificacion_registrada.id:
        nuevo_id_staff = random.choice(staff).id

    certificaciones_manager.modificar_id_staff(ultima_certificacion_registrada, id_staff, nuevo_id_staff)

    assert ultima_certificacion_registrada.id_staff == nuevo_id_staff
    assert ultima_certificacion_registrada.descripcion == certificacion.descripcion
    assert ultima_certificacion_registrada.licencia_hasta == certificacion.licencia_hasta

def test_modificar_certificacion_staff_invalido(db_conectada: DBManager, certificaciones_manager: CertificacionesStaffManager, staff: list[StaffDesdeDB], id_staff: int) -> None:
    certificacion: CertificacionStaffBase = generar_certificaciones(1, staff)[0]

    certificaciones_manager.registrar_certificacion(id_staff, certificacion)
    ultima_certificacion_registrada = CertificacionStaffDesdeDB(*db_conectada.consultar_ultima_fila("certificaciones_staff", COLUMNAS_CERTIFICACIONES_STAFF))

    nuevo_id_staff = random.choice(staff).id
    while nuevo_id_staff == ultima_certificacion_registrada.id:
        nuevo_id_staff = random.choice(staff).id

    ID_STAFF = 999

    with pytest.raises(Exception, match=ERROR_STAFF_INVALIDO):
        certificaciones_manager.modificar_id_staff(ultima_certificacion_registrada, ID_STAFF, nuevo_id_staff)

def test_modificar_certificacion_descripcion_correcta(db_conectada: DBManager, certificaciones_manager: CertificacionesStaffManager, staff: list[StaffDesdeDB], id_staff: int) -> None:
    certificacion: CertificacionStaffBase = generar_certificaciones(1, staff)[0]

    certificaciones_manager.registrar_certificacion(id_staff, certificacion)
    ultima_certificacion_registrada = CertificacionStaffDesdeDB(*db_conectada.consultar_ultima_fila("certificaciones_staff", COLUMNAS_CERTIFICACIONES_STAFF))

    nueva_descripcion = "Licencia profesional X"
    certificaciones_manager.modificar_descripcion(ultima_certificacion_registrada, id_staff, nueva_descripcion)

    ultima_certificacion_registrada = CertificacionStaffDesdeDB(*db_conectada.consultar_ultima_fila("certificaciones_staff", COLUMNAS_CERTIFICACIONES_STAFF))

    assert ultima_certificacion_registrada.id_staff == certificacion.id_staff
    assert ultima_certificacion_registrada.descripcion == nueva_descripcion
    assert ultima_certificacion_registrada.licencia_hasta == certificacion.licencia_hasta

def test_modificar_certificacion_descripcion_invalida(db_conectada: DBManager, certificaciones_manager: CertificacionesStaffManager, staff: list[StaffDesdeDB], id_staff: int) -> None:
    certificacion: CertificacionStaffBase = generar_certificaciones(1, staff)[0]

    certificaciones_manager.registrar_certificacion(id_staff, certificacion)
    ultima_certificacion_registrada = CertificacionStaffDesdeDB(*db_conectada.consultar_ultima_fila("certificaciones_staff", COLUMNAS_CERTIFICACIONES_STAFF))

    nueva_descripcion = 123

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        certificaciones_manager.modificar_descripcion(ultima_certificacion_registrada, id_staff, nueva_descripcion)
    
def test_modificar_certificacion_vencimiento_correcto(db_conectada: DBManager, certificaciones_manager: CertificacionesStaffManager, staff: list[StaffDesdeDB], id_staff: int) -> None:
    certificacion: CertificacionStaffBase = generar_certificaciones(1, staff)[0]

    certificaciones_manager.registrar_certificacion(id_staff, certificacion)
    ultima_certificacion_registrada = CertificacionStaffDesdeDB(*db_conectada.consultar_ultima_fila("certificaciones_staff", COLUMNAS_CERTIFICACIONES_STAFF))

    nueva_licencia_hasta = datetime(2090, 1, 1)
    certificaciones_manager.modificar_vencimiento(ultima_certificacion_registrada, id_staff, nueva_licencia_hasta)

    ultima_certificacion_registrada = CertificacionStaffDesdeDB(*db_conectada.consultar_ultima_fila("certificaciones_staff", COLUMNAS_CERTIFICACIONES_STAFF))

    assert ultima_certificacion_registrada.id_staff == certificacion.id_staff
    assert ultima_certificacion_registrada.descripcion == certificacion.descripcion
    assert ultima_certificacion_registrada.licencia_hasta == nueva_licencia_hasta

def test_modificar_certificacion_vencimiento_invalida(db_conectada: DBManager, certificaciones_manager: CertificacionesStaffManager, staff: list[StaffDesdeDB], id_staff: int) -> None: 
    certificacion: CertificacionStaffBase = generar_certificaciones(1, staff)[0]

    certificaciones_manager.registrar_certificacion(id_staff, certificacion)
    ultima_certificacion_registrada = CertificacionStaffDesdeDB(*db_conectada.consultar_ultima_fila("certificaciones_staff", COLUMNAS_CERTIFICACIONES_STAFF))

    nueva_licencia_hasta = "ABC"

    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        certificaciones_manager.modificar_vencimiento(ultima_certificacion_registrada, id_staff, nueva_licencia_hasta)