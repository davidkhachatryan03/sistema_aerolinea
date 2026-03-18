import pytest, random
from src.managers import *
from src.tipos import *
from src.entidades import *
from src.querys import *
from src.columnas import *
from src.errores import *
from src.GeneradorDatos import GeneradorDatos

def registrar_pasajeros(generador_datos: GeneradorDatos, pasajeros_manager: TablaManager, cant: int, id_staff: int) -> None:
    pasajeros_generados = generador_datos.generar_pasajeros(cant)
    for pasajero in pasajeros_generados:
        pasajeros_manager.agregar_fila(id_staff, pasajero.to_dict())

def generar_documentos(generador_datos: GeneradorDatos, pasajeros: list[PasajeroDesdeDB]) -> list[DocumentoBase]:
    documentos: list[DocumentoBase] = generador_datos.generar_documentos(pasajeros)
    return documentos

def test_registrar_documento_correcto(db_conectada: DBManager, generador_datos: GeneradorDatos, documentos_manager: DocumentosManager, pasajeros_manager: TablaManager, id_staff: int) -> None:
    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)
    ultimo_pasajero_registrado: PasajeroDesdeDB = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))

    documento: DocumentoBase = generador_datos.generar_documentos([ultimo_pasajero_registrado])[0]
    documentos_manager.registrar_documento(id_staff, documento)

    ultimo_documento_registrado = DocumentoDesdeDB(*db_conectada.consultar_ultima_fila("documentos", COLUMNAS_DOCUMENTOS))

    assert ultimo_documento_registrado.num_documento == documento.num_documento
    assert ultimo_documento_registrado.fecha_vencimiento == documento.fecha_vencimiento
    assert ultimo_documento_registrado.pais_emision == documento.pais_emision
    assert ultimo_documento_registrado.id_pasajero == documento.id_pasajero
    assert ultimo_documento_registrado.id_tipo_documento == documento.id_tipo_documento

def test_registrar_documento_staff_invalido(db_conectada: DBManager, generador_datos: GeneradorDatos, documentos_manager: DocumentosManager, pasajeros_manager: TablaManager, id_staff: int) -> None:
    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)
    ultimo_pasajero_registrado: PasajeroDesdeDB = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))

    documento: DocumentoBase = generador_datos.generar_documentos([ultimo_pasajero_registrado])[0]

    ID_STAFF = 999 # cambio el id_staff por uno erróneo.

    with pytest.raises(Exception, match=ERROR_STAFF_INVALIDO):
        documentos_manager.registrar_documento(ID_STAFF, documento)

def test_modificar_num_documento_correcto(db_conectada: DBManager, generador_datos: GeneradorDatos, documentos_manager: DocumentosManager, pasajeros_manager: TablaManager, id_staff: int) -> None:
    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)
    ultimo_pasajero_registrado: PasajeroDesdeDB = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))

    documento: DocumentoBase = generador_datos.generar_documentos([ultimo_pasajero_registrado])[0]
    documentos_manager.registrar_documento(id_staff, documento)

    ultimo_documento_registrado = DocumentoDesdeDB(*db_conectada.consultar_ultima_fila("documentos", COLUMNAS_DOCUMENTOS))

    nuevo_num_documento = "AA1945723"
    documentos_manager.modificar_num_documento(ultimo_documento_registrado.id, id_staff, nuevo_num_documento)

    ultimo_documento_registrado = DocumentoDesdeDB(*db_conectada.consultar_ultima_fila("documentos", COLUMNAS_DOCUMENTOS))

    assert ultimo_documento_registrado.num_documento == nuevo_num_documento
    assert ultimo_documento_registrado.fecha_vencimiento == documento.fecha_vencimiento
    assert ultimo_documento_registrado.pais_emision == documento.pais_emision
    assert ultimo_documento_registrado.id_pasajero == documento.id_pasajero
    assert ultimo_documento_registrado.id_tipo_documento == documento.id_tipo_documento

def test_modificar_num_documento_invalido(db_conectada: DBManager, generador_datos: GeneradorDatos, documentos_manager: DocumentosManager, pasajeros_manager: TablaManager, id_staff: int) -> None:
    registrar_pasajeros(generador_datos, pasajeros_manager, 1, id_staff)
    ultimo_pasajero_registrado: PasajeroDesdeDB = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))

    documento: DocumentoBase = generador_datos.generar_documentos([ultimo_pasajero_registrado])[0]
    documentos_manager.registrar_documento(id_staff, documento)

    ultimo_documento_registrado = DocumentoDesdeDB(*db_conectada.consultar_ultima_fila("documentos", COLUMNAS_DOCUMENTOS))

    nuevo_num_documento = 34512
    with pytest.raises(Exception, match=ERROR_FORMATO_DATOS):
        documentos_manager.modificar_num_documento(ultimo_documento_registrado.id, id_staff, nuevo_num_documento)