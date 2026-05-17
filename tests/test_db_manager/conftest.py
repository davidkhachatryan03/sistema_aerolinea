import pytest
from src.common import DBManager

@pytest.fixture
def db_test(db_manager: DBManager) -> DBManager:
    return db_manager