import pytest
from init_db import main
from src.managers import DBManager

@pytest.fixture(scope="session", autouse=True)
def config():
    main(test=True)

@pytest.fixture
def db_conectada():
    db_conectada = DBManager()
    db_conectada.conectar()
    db_conectada.execute("USE aerolinea")
    yield db_conectada
    db_conectada.desconectar()