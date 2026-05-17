import pytest
from src.common import DBManager

def test_connect(db_test: DBManager) -> None:
    db_test.connect()

    assert db_test.connection.is_connected() == True