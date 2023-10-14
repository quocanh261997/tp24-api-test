import re

from pydantic import BaseModel
from typing import Optional
from datetime import date


def to_camel(string: str) -> str:
    # Convert snake_case to camelCase
    words = string.split('_')
    return words[0] + ''.join(word.capitalize() for word in words[1:])


class ReceivableCreate(BaseModel):
    reference: str
    currency_code: str
    issue_date: date
    opening_value: float
    paid_value: float
    due_date: date
    closed_date: Optional[date] = None
    cancelled: Optional[bool] = None
    debtor_name: str
    debtor_reference: str
    debtor_address1: Optional[str] = None
    debtor_address2: Optional[str] = None
    debtor_town: Optional[str] = None
    debtor_state: Optional[str] = None
    debtor_zip: Optional[str] = None
    debtor_country_code: str
    debtor_registration_number: Optional[str] = None

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class ReceivableSummary(BaseModel):
    total_open_invoices: int
    total_closed_invoices: int
    total_open_value: float
    total_closed_value: float
