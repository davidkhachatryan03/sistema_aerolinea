import pytest
from init_db import main
from src.managers import *
from src.entidades import *
from src.tipos import *
from src.querys import *
from src.GeneradorDatos import GeneradorDatos

@pytest.fixture(scope="session", autouse=True)
def config():
    main(test=True)

@pytest.fixture
def db_conectada():
    db_conectada = DBManager()
    db_conectada.conectar()
    db_conectada.execute("USE aerolinea")
    yield db_conectada
    db_conectada.borrar_tabla("certificaciones_staff")
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