import pytest
from src.entities import BoardingPassCreated

def test_valid_boarding_pass(valid_boarding_pass: dict) -> None:
    boarding_pass_created = BoardingPassCreated(**valid_boarding_pass)

    assert boarding_pass_created.issue_datetime == valid_boarding_pass["issue_datetime"]
    assert boarding_pass_created.boarding_datetime == valid_boarding_pass["boarding_datetime"]
    assert boarding_pass_created.current_status_id == valid_boarding_pass["current_status_id"]
    assert boarding_pass_created.ticket_id == valid_boarding_pass["ticket_id"]

@pytest.mark.parametrize("field, value, expected_exception", [
    ("issue_datetime", 123, TypeError),
    ("boarding_datetime", 123, TypeError),
    ("current_status_id", "123", TypeError),
    ("current_status_id", 0, ValueError),
    ("current_status_id", -100, ValueError),
    ("ticket_id", "123", TypeError),
    ("ticket_id", 0, ValueError),
    ("ticket_id", -100, ValueError),
])

def test_invalid_boarding_pass(valid_boarding_pass: dict, field: str, value, expected_exception) -> None:
    test_data = valid_boarding_pass.copy()
    test_data[field] = value

    with pytest.raises(expected_exception):
        BoardingPassCreated(**test_data)