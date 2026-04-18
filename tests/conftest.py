import pytest, random
from init_db import main
from collections.abc import Callable
from src.managers import *
from src.entidades import *
from src.tipos import *
from src.querys import *
from src.GeneradorDatos import GeneradorDatos
from src.columnas import *

@pytest.fixture(scope="session", autouse=True)
def config():
    main(test=True)

@pytest.fixture
def db_conectada():
    db_conectada = DBManager()
    db_conectada.conectar()
    db_conectada.execute("USE aerolinea")
    yield db_conectada
    db_conectada.borrar_tabla("asignaciones_vuelos")
    db_conectada.borrar_tabla("tarjetas_embarque")
    db_conectada.borrar_tabla("documentos")
    db_conectada.borrar_tabla("ventas")
    db_conectada.borrar_tabla("vuelos")
    db_conectada.borrar_tabla("pasajeros")
    db_conectada.commit()
    db_conectada.desconectar()

@pytest.fixture
def generador_datos(db_conectada: DBManager) -> GeneradorDatos:
    generador_datos = GeneradorDatos(db_conectada)
    return generador_datos

@pytest.fixture
def ventas_manager(db_conectada: DBManager) -> VentasManager:
    ventas_manager = VentasManager(db_conectada)
    return ventas_manager

@pytest.fixture
def pasajeros_manager(db_conectada: DBManager) -> TablaManager:
    pasajeros_manager = TablaManager("pasajeros", db_conectada)
    return pasajeros_manager

@pytest.fixture
def vuelos_manager(db_conectada: DBManager) -> VuelosManager:
    vuelos_manager = VuelosManager(db_conectada)
    return vuelos_manager

@pytest.fixture
def documentos_manager(db_conectada: DBManager) -> DocumentosManager:
    documentos_manager = DocumentosManager(db_conectada)
    return documentos_manager

@pytest.fixture
def tarjetas_embarque_manager(db_conectada: DBManager) -> TarjetasEmbarqueManager:
    tarjetas_embarque_manager = TarjetasEmbarqueManager(db_conectada)
    return tarjetas_embarque_manager

@pytest.fixture
def certificaciones_manager(db_conectada: DBManager) -> CertificacionesStaffManager:
    certificaciones_manager = CertificacionesStaffManager(db_conectada)
    return certificaciones_manager

@pytest.fixture
def asignaciones_vuelos_manager(db_conectada: DBManager) -> AsignacionesVuelosManager:
    asignaciones_vuelos_manager = AsignacionesVuelosManager(db_conectada)
    return asignaciones_vuelos_manager

@pytest.fixture
def id_staff(id: int=25) -> int:
    ID_STAFF = id
    return ID_STAFF

@pytest.fixture
def rutas(db_conectada: DBManager) -> list[RutaDesdeDB]:
    rutas: list[RutaDesdeDB] = []

    consulta_rutas: list[FilaRuta] = db_conectada.consultar(OBTENER_TODAS_LAS_RUTAS)
    for ruta in consulta_rutas:
        rutas.append(RutaDesdeDB(*ruta))

    return rutas

@pytest.fixture
def aviones(db_conectada: DBManager) -> list[AvionDesdeDB]:
    aviones: list[AvionDesdeDB] = []

    consulta_aviones: list[FilaAvion] = db_conectada.consultar(OBTENER_TODOS_LOS_AVIONES)
    for avion in consulta_aviones:
        aviones.append(AvionDesdeDB(*avion))

    return aviones

@pytest.fixture
def staff(db_conectada: DBManager) -> list[StaffDesdeDB]:
    staff: list[StaffDesdeDB] = []

    consulta_staff: list[FilaStaff] = db_conectada.consultar(OBTENER_TODO_EL_STAFF)
    for empleado in consulta_staff:
        staff.append(StaffDesdeDB(*empleado))
    
    return staff

@pytest.fixture
def vuelo_valido_sin_registrar(generador_datos: GeneradorDatos, vuelos_manager: VuelosManager, rutas: list[RutaDesdeDB], aviones: list[AvionDesdeDB]) -> Callable[[], VueloBase]:

    def _crear() -> VueloBase:
        while True:
            vuelo_generado = generador_datos.generar_vuelos(cant=1, rutas=rutas, aviones=aviones)[0]

            if vuelos_manager._verificar_avion(vuelo_generado.id_avion, vuelo_generado.id_ruta, vuelo_generado.fecha_partida_programada, vuelo_generado.fecha_arribo_programada):
                
                return vuelo_generado
    
    return _crear

@pytest.fixture
def vuelo_registrado(db_conectada: DBManager, vuelos_manager: VuelosManager, vuelo_valido_sin_registrar: Callable[[], VueloBase], id_staff: int) -> Callable[[], tuple[VueloBase, VueloDesdeDB]]:

    def _crear() -> tuple[VueloBase, VueloDesdeDB]:
        vuelo_generado = vuelo_valido_sin_registrar()
        vuelos_manager.registrar_vuelo(id_staff, vuelo_generado)
        ultimo_vuelo_registrado = VueloDesdeDB(*db_conectada.consultar_ultima_fila("vuelos", COLUMNAS_VUELOS))

        return vuelo_generado, ultimo_vuelo_registrado
    
    return _crear

@pytest.fixture
def pasajero_valido_sin_registrar(generador_datos: GeneradorDatos) -> Callable[[], PasajeroBase]:

    def _crear() -> PasajeroBase:
        pasajero_generado = generador_datos.generar_pasajeros(cant=1)[0]

        return pasajero_generado
    
    return _crear

@pytest.fixture
def pasajero_registrado(db_conectada: DBManager, pasajeros_manager: TablaManager, pasajero_valido_sin_registrar: Callable[[], PasajeroBase], id_staff: int) -> Callable[[], tuple[PasajeroBase, PasajeroDesdeDB]]:

    def _crear() -> tuple[PasajeroBase, PasajeroDesdeDB]:
        pasajero_generado = pasajero_valido_sin_registrar()
        pasajeros_manager.agregar_fila(id_staff, pasajero_generado)
        ultimo_pasajero_registrado = PasajeroDesdeDB(*db_conectada.consultar_ultima_fila("pasajeros", COLUMNAS_PASAJEROS))

        return pasajero_generado, ultimo_pasajero_registrado
    
    return _crear

@pytest.fixture
def venta_valida_sin_registrar(generador_datos: GeneradorDatos, vuelo_registrado: Callable[[], tuple[VueloBase, VueloDesdeDB]], pasajero_registrado: Callable[[], tuple[PasajeroBase, PasajeroDesdeDB]]) -> Callable[[], VentaBase]:

    def _crear() -> VentaBase:
        venta_generada = generador_datos.generar_ventas(cant=1, vuelos=[vuelo_registrado()[1]], pasajeros=[pasajero_registrado()[1]])[0]

        return venta_generada
    
    return _crear

@pytest.fixture
def venta_registrada(db_conectada: DBManager, ventas_manager: VentasManager, venta_valida_sin_registrar: Callable[[], VentaBase], id_staff: int) -> Callable[[], tuple[VentaBase, VentaDesdeDB]]:

    def _crear() -> tuple[VentaBase, VentaDesdeDB]:
        venta_generada = venta_valida_sin_registrar()
        ventas_manager.registrar_venta(id_staff, venta_generada)
        ultima_venta_registrada = VentaDesdeDB(*db_conectada.consultar_ultima_fila("ventas", COLUMNAS_VENTAS))

        return venta_generada, ultima_venta_registrada
    
    return _crear

@pytest.fixture
def tarjeta_embarque_valida_sin_registrar(generador_datos: GeneradorDatos, venta_registrada: Callable[[], tuple[VentaBase, VentaDesdeDB]]) -> Callable[[], TarjetaEmbarqueBase]:

    def _crear() -> TarjetaEmbarqueBase:
        venta: VentaDesdeDB = venta_registrada()[1]
        tarjeta_embarque_generada: TarjetaEmbarqueBase = generador_datos.generar_tarjetas_embarque([venta])[0]

        return tarjeta_embarque_generada
    
    return _crear

@pytest.fixture
def tarjeta_embarque_registrada(db_conectada: DBManager, tarjetas_embarque_manager: TarjetasEmbarqueManager, tarjeta_embarque_valida_sin_registrar: Callable[[], TarjetaEmbarqueBase], id_staff: int) -> Callable[[], tuple[TarjetaEmbarqueBase, TarjetaEmbarqueDesdeDB]]:

    def _crear() -> tuple[TarjetaEmbarqueBase, TarjetaEmbarqueDesdeDB]:
        tarjeta_embarque_generada = tarjeta_embarque_valida_sin_registrar()
        tarjetas_embarque_manager.registrar_tarjeta_embarque(id_staff, tarjeta_embarque_generada)
        ultima_tarjeta_embarque_registrada = TarjetaEmbarqueDesdeDB(*db_conectada.consultar_ultima_fila("tarjetas_embarque", COLUMNAS_TARJETAS_EMBARQUE))

        return tarjeta_embarque_generada, ultima_tarjeta_embarque_registrada
    
    return _crear

@pytest.fixture
def documento_valido_sin_registrar(generador_datos: GeneradorDatos, pasajero_registrado: Callable[[], tuple[PasajeroBase, PasajeroDesdeDB]]) -> Callable[[], DocumentoBase]:

    def _crear() -> DocumentoBase:
        pasajero: PasajeroDesdeDB = pasajero_registrado()[1]
        documento_generado: DocumentoBase = generador_datos.generar_documentos([pasajero])[0]
        
        return documento_generado
    
    return _crear

@pytest.fixture
def documento_registrado(db_conectada: DBManager, documentos_manager: DocumentosManager, documento_valido_sin_registrar: Callable[[], DocumentoBase], id_staff: int) -> Callable[[], tuple[DocumentoBase, DocumentoDesdeDB]]:

    def _crear() -> tuple[DocumentoBase, DocumentoDesdeDB]:
        documento_generado = documento_valido_sin_registrar()
        documentos_manager.registrar_documento(id_staff, documento_generado)
        ultimo_documento_registrado = DocumentoDesdeDB(*db_conectada.consultar_ultima_fila("documentos", COLUMNAS_DOCUMENTOS))

        return documento_generado, ultimo_documento_registrado
    
    return _crear

def generar_certificacion(staff: list[StaffDesdeDB]) -> CertificacionStaffBase:
    id_staff: int = random.choice(staff).id
    descripcion = "Licencia X"
    licencia_hasta = datetime(2060, 1, 1)

    certificacion = CertificacionStaffBase(id_staff, descripcion, licencia_hasta)

    return certificacion

@pytest.fixture
def certificacion_valida_sin_registrar(staff: list[StaffDesdeDB]) -> Callable[[], CertificacionStaffBase]:

    def _crear() -> CertificacionStaffBase:
        certificacion_generada: CertificacionStaffBase = generar_certificacion(staff)

        return certificacion_generada
    
    return _crear

@pytest.fixture
def certificacion_registrada(db_conectada: DBManager, certificaciones_manager: CertificacionesStaffManager, certificacion_valida_sin_registrar: Callable[[], CertificacionStaffBase], id_staff: int) -> Callable[[], tuple[CertificacionStaffBase, CertificacionStaffDesdeDB]]:

    def _crear() -> tuple[CertificacionStaffBase, CertificacionStaffDesdeDB]:
        certificacion_generada = certificacion_valida_sin_registrar()
        certificaciones_manager.registrar_certificacion(id_staff, certificacion_generada)
        ultima_certificacion_generada = CertificacionStaffDesdeDB(*db_conectada.consultar_ultima_fila("certificaciones_staff", COLUMNAS_CERTIFICACIONES_STAFF))

        return certificacion_generada, ultima_certificacion_generada
    
    return _crear