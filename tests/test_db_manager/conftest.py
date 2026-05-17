import pytest
from src.common import DBManager

@pytest.fixture
def db_test() -> DBManager:
    db_manager = DBManager()
    return db_manager