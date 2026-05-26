from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from decimal import Decimal
from datetime import date

class PassengerRequest(BaseModel):
    full_name: str
    birth_date: date
    email: str
    phone_number: int
    document_number: str
    issue_country: str
    document_type_id: int