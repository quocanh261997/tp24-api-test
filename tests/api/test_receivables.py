def test_create_receivable_valid(test_client, valid_receivable_data):
    response = test_client.post("/api/receivables", json=[valid_receivable_data])

    assert response.status_code == 201
    assert "reference" in response.json()[0]
    assert response.json()[0]["reference"] == valid_receivable_data["reference"]


def test_create_receivable_invalid(test_client, invalid_receivable_data):
    response = test_client.post("/api/receivables", json=[invalid_receivable_data])

    assert response.status_code == 422


def test_get_receivable_summary_no_filter(test_client, valid_receivable_data):
    # Add a receivable before attempting to retrieve it
    test_client.post("/api/receivables", json=[valid_receivable_data])

    response = test_client.get("/api/receivables/summary")

    assert response.status_code == 200
    assert "open_invoices_value" in response.json()
    assert "closed_invoices_value" in response.json()


def test_get_receivable_summary_with_filter_valid(test_client, valid_receivable_data):
    # Add a receivable before attempting to retrieve it
    test_client.post("/api/receivables", json=[valid_receivable_data])

    params = {
        "debtorName": valid_receivable_data["debtorName"],
        "untilDate": "2023-10-01T00:00:00Z"
    }
    response = test_client.get("/api/receivables/summary", params=params)

    assert response.status_code == 200
    assert "open_invoices_value" in response.json()
    assert "closed_invoices_value" in response.json()


def test_get_receivable_summary_with_filter_invalid(test_client, valid_receivable_data):
    # Add a receivable before attempting to retrieve it
    test_client.post("/api/receivables", json=[valid_receivable_data])

    params = {
        # Invalid filter
        "invalidFilter": "someValue"
    }
    response = test_client.get("/api/receivables/summary", params=params)

    assert response.status_code == 422
