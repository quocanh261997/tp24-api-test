import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.api.main import app  # Adjust your import according to your project structure
from app.models import receivables
from tests.utils import clear_receivables_data

load_dotenv()

SQLALCHEMY_TEST_DATABASE_URL = os.getenv("DATABASE_TEST_URL", "sqlite:///./test-1.db")

try:
    engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}, future=True)
    print(f"Engine ID: {id(engine)}")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"An error occurred: {str(e)}")


@pytest.fixture(scope="function")
def test_db():
    # create tables
    receivables.Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    print(f"[test_db] Engine ID: {id(engine)}")
    print(f"[test_db] Session ID before yield: {id(db_session)}")
    yield db_session
    print(f"[test_db] Session ID after yield: {id(db_session)}")
    db_session.close()
    receivables.Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_client(test_db):
    def _get_db_override():
        yield test_db  # Simply yield the provided `test_db` instance.

    app.dependency_overrides[get_db] = _get_db_override

    headers = {"x-api-key": os.getenv("API_KEY")}
    client = TestClient(app)
    client.headers.update(headers)  # Update headers.

    yield client

    app.dependency_overrides = {}  # Ensure we clean up after ourselves by resetting the overrides.


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
def valid_receivable_data_2():
    data = [
        {
            "reference": "INV12345",
            "currencyCode": "USD",
            "issueDate": "2023-11-01",
            "openingValue": 1000.00,
            "paidValue": 500.00,
            "dueDate": "2023-12-01",
            "debtorName": "tommy",
            "debtorReference": "CXYZ678",
            "debtorCountryCode": "US",
            "debtorRegistrationNumber": "RN123456"
        },
        {
            "reference": "INV12346",
            "currencyCode": "USD",
            "issueDate": "2023-10-01",
            "openingValue": 845.3,
            "paidValue": 845.3,
            "closedDate": "2024-01-01",
            "dueDate": "2024-02-01",
            "debtorName": "brad",
            "debtorReference": "CXYZ679",
            "debtorCountryCode": "US",
            "debtorRegistrationNumber": "RN123457"
        },
        {
            "reference": "INV12347",
            "currencyCode": "USD",
            "issueDate": "2023-12-01",
            "openingValue": 5000.00,
            "paidValue": 1500.00,
            "dueDate": "2024-11-01",
            "debtorName": "tommy",
            "debtorReference": "CXYZ678",
            "debtorCountryCode": "US",
            "debtorRegistrationNumber": "RN123456"
        }
    ]
    return data


@pytest.fixture
def invalid_receivable_data():
    data = {
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
    }
    return data


@pytest.fixture(scope="function")
def clean_up_after_test(test_db):
    yield clear_receivables_data(test_db)
