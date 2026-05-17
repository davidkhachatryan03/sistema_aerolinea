import pytest, os
from src.common import DBManager
from src.common.exceptions import CursorNotFound, DatabaseError, SQLFileNotFound
from typing import cast

def test_connections(db_test: DBManager) -> None:
    with pytest.raises(AttributeError):
        db_test.connection

    with pytest.raises(AttributeError):
        db_test.cursor

    db_test.connect()

    assert db_test.connection.is_connected() == True

    db_test.disconnect()

    assert db_test.connection.is_connected() == False

def test_execute_sql_file(db_test: DBManager) -> None:
    db_test.connect()
    route = os.path.join(os.getcwd(), "tests/test_db_manager/valid_sql_file_test.sql")

    db_test.execute_sql_file(route)

    row: tuple[int] = cast(tuple, db_test.cursor.fetchone())
    result: int = row[0]

    assert result == 1

def test_execute_sql_file_invalid_route(db_test: DBManager) -> None:
    db_test.connect()

    with pytest.raises(SQLFileNotFound):
        db_test.execute_sql_file("")

def test_execute_sql_file_permission_denied(db_test: DBManager) -> None:
    db_test.connect()

    with pytest.raises(DatabaseError):
        db_test.execute_sql_file(os.getcwd())

def test_execute_sql_file_invalid_syntax(db_test: DBManager) -> None:
    db_test.connect()
    route = os.path.join(os.getcwd(), "tests/test_db_manager/invalid_sql_file_test.sql")

    with pytest.raises(Exception):
        db_test.execute_sql_file(route)