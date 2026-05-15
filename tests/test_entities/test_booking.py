import pytest
from src.entities import BookingCreated
from decimal import Decimal

def test_valid_booking(valid_booking: dict) -> None:
    booking_created = BookingCreated(**valid_booking)

    assert booking_created.booking_reference == valid_booking["booking_reference"]
    assert booking_created.booking_datetime == valid_booking["booking_datetime"]
    assert booking_created.paid_amount_usd == valid_booking["paid_amount_usd"]
    assert booking_created.current_status_id == valid_booking["current_status_id"]

@pytest.mark.parametrize("field, value, expected_exception", [
    ("booking_reference", 123, TypeError),
    ("booking_reference", "   ", ValueError),
    ("booking_reference", "", ValueError),
    ("booking_reference", "ABCD1234567", ValueError),
    ("booking_datetime", 123, TypeError),
    ("paid_amount_usd", "123", TypeError),
    ("paid_amount_usd", Decimal("0"), ValueError),
    ("paid_amount_usd", Decimal("-100"), ValueError),
    ("current_status_id", "123", TypeError),
    ("current_status_id", 0, ValueError),
    ("current_status_id", -100, ValueError),
])

def test_invalid_booking(valid_booking: dict, field: str, value, expected_exception) -> None:
    test_data = valid_booking.copy()
    test_data[field] = value

    with pytest.raises(expected_exception):
        BookingCreated(**test_data)