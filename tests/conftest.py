import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from app.api.main import app  # Adjust your import according to your project structure

load_dotenv()


@pytest.fixture(scope="module")
def test_client():
    headers = {"x-api-key": os.getenv("API_KEY")}
    client = TestClient(app, headers=headers)
    yield client


@pytest.fixture
def valid_receivable_data():
    data = {
        "reference": "INV12345",
        "currencyCode": "USD",
        "issueDate": "2023-10-01",
        "openingValue": 1000.00,
        "paidValue": 500.00,
        "dueDate": "2023-11-01",
        "debtorName": "Client XYZ",
        "debtorReference": "CXYZ678",
        "debtorCountryCode": "US",
        "debtorRegistrationNumber": "RN123456"
    }
    return data


@pytest.fixture
def invalid_receivable_data():
    data = [{
        # Missing "reference" field
        "currencyCode": "USD",
        "issueDate": "2023-10-01",
        # Invalid data type for "openingValue" (should be float)
        "openingValue": "invalid_value",
        "paidValue": 500.00,
        "dueDate": "2023-11-01",
        "debtorName": "Client XYZ",
        "debtorReference": "CXYZ678",
        "debtorCountryCode": "US",
        # Missing "debtorRegistrationNumber" field
    }]
    return data
