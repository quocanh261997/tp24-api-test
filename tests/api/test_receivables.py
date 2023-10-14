def test_create_receivable_valid(test_client, valid_receivable_data, clean_up_after_test):
    response = test_client.post("/api/receivables", json=[valid_receivable_data])

    assert response.status_code == 201
    assert "reference" in response.json()[0]
    assert response.json()[0]["reference"] == valid_receivable_data["reference"]


def test_create_receivable_unauthorized(test_client, valid_receivable_data, clean_up_after_test):
    test_client.headers.clear()
    response = test_client.post("/api/receivables", json=[valid_receivable_data])

    assert response.status_code == 401


def test_create_receivable_invalid(test_client, invalid_receivable_data, clean_up_after_test):
    response = test_client.post("/api/receivables", json=[invalid_receivable_data])

    assert response.status_code == 422


def test_get_receivable_summary_no_filter(test_client, valid_receivable_data_2, clean_up_after_test):
    # Add a receivable before attempting to retrieve it
    test_client.post("/api/receivables", json=valid_receivable_data_2)

    response = test_client.get("/api/receivables/summary")

    assert response.status_code == 200
    assert response.json()["total_open_invoices"] == 2
    assert response.json()["total_closed_invoices"] == 1
    assert response.json()["total_open_value"] == 6000.0
    assert response.json()["total_closed_value"] == 845.3


def test_get_receivable_summary_with_filter_valid(test_client, valid_receivable_data_2, clean_up_after_test):
    # Add a receivable before attempting to retrieve it
    test_client.post("/api/receivables", json=valid_receivable_data_2)

    params = {
        "debtorName": "tommy",
        "untilDate": "2024-03-01"
    }
    response = test_client.get("/api/receivables/summary", params=params)

    assert response.status_code == 200
    assert response.json()["total_open_invoices"] == 1
    assert response.json()["total_closed_invoices"] == 0
    assert response.json()["total_open_value"] == 1000.0
    assert response.json()["total_closed_value"] == 0.0


def test_get_receivable_summary_with_filter_invalid(test_client, valid_receivable_data, clean_up_after_test):
    # Add a receivable before attempting to retrieve it
    test_client.post("/api/receivables", json=[valid_receivable_data])

    params = {
        # Invalid filter
        "invalidFilter": "someValue"
    }
    response = test_client.get("/api/receivables/summary", params=params)

    assert response.status_code == 200  # Invalid filter is ignored
