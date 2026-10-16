import pytest
import responses
from src.inventory import Item

BASE_URL = "http://localhost:5000/inventory"


def test_health_check(test_client):
    """GIVEN a Flask application configured for testing
    WHEN the "/api/health" page is requested via GET
    THEN check that the status is valid"""
    response = test_client.get("/api/health")
    assert response.status_code == 200
    assert {"status": "ok"} == response.get_json()


@responses.activate
def test_get_inventory(test_client):
    """GIVEN a Flask application configured for testing
    WHEN the "/inventory" page is requested via GET
    THEN check that a list of Item objects is returned"""
    #  set up fake response data
    responses.add(
        responses.GET,
        BASE_URL,
        json=[Item("Cereal", "000", 1).to_dict(), Item("Milk", "111", 8).to_dict()],
        status=200,
    )

    #  Call get
    result = test_client.get("/inventory")
    assert result.status_code == 200
    #  Verify data
    data = result.get_json()
    assert type(data) == list
    for item in data:
        assert item["name"] in ["Cereal", "Milk"]


def test_get_by_id(test_client):
    """GIVEN a Flask app and an ID number
    WHEN the "/inventory/id/" page is requested via GET
    THEN check that a single Item object is returned
        OR invalid ID returns 404"""
    #  set up fake response data
    responses.add(
        responses.GET,
        f"{BASE_URL}/0",
        json={
            "id": "abc",
            "name": "Cereal",
            "barcode": "000",
            "brand": "General Mills",
            "quantity": 1,
        },
        status=200,
    )

    #  Call get
    result = test_client.get("/inventory/0")
    #  Verify data
    assert result.status_code == 200
    data = result.get_json()
    assert data["id"] == "abc"
    assert data["name"] == "Cereal"
    assert data["barcode"] == "000"
    assert data["brand"] == "General Mills"
    assert data["quantity"] == 1

    #  Fake response for invalid object
    responses.add(responses.GET, f"{BASE_URL}/420", status=404)
    #  Call get
    result = test_client.get("/inventory/420")
    assert result.status_code == 404


def test_post_item(test_client):
    """GIVEN a Flask app and a new Item object
    WHEN the "/inventory" page is POSTed to
    THEN check that:
        - A 201 response is generated on valid JSON
        - A 400 response is generated on invalid JSON"""
    #  Call with valid JSON
    result = test_client.post(
        "/inventory",
        {"name": "Cereal", "barcode": "000", "brand": "General Mills", "quantity": 1},
    )
    assert result.status_code == 201
    
    #  Call with invalid JSONs
    result = test_client.post(
        "/inventory",
        {"barcode": "000", "brand": "General Mills", "quantity": 1},
    )  # No name
    assert result.status_code == 400
    
    result = test_client.post(
        "/inventory",
        {"name": "Cereal", "brand": "General Mills", "quantity": 1},
    )  # No barcode
    assert result.status_code == 400
    
    result = test_client.post(
        "/inventory",
        {"name": "Cereal", "barcode": "000", "brand": "General Mills"},
    )  # No quantity
    assert result.status_code == 400


def test_patch_item(test_client):
    """GIVEN a Flask app and an existing Item object
    WHEN the "/inventory/id/" page is PATCHed
    THEN check that:
        - A 200 response is generated on successful patch
        - A 400 response is generated on invalid JSON
        - A 404 response is generated on non-existing ID"""
    #  Check patch with valid JSONs
    result = test_client.patch("/inventory/0", {"name": "Resee's Puffs"})
    assert result.status_code == 200
    updated_item = test_client.get("/inventory/0").get_json()
    assert updated_item["name"] == "Resee's Puffs"
    
    #  Check patch with invalid JSON or ID
    result = test_client.patch("/inventory/0", {})
    assert result.status_code == 400
    
    result = test_client.patch("/inventory/420", {"name": "Fake Item"})
    assert result.status_code == 404


def test_delete_item(test_client):
    """GIVEN a Flask app and an existing Item object
    WHEN the "/inventory/id/" page is DELETEd
    THEN check that:
        - A 204 response is generated on successful patch
        - A 404 response is generated on non-existing ID"""
    #  Check delete on valid ID
    result = test_client.delete("/inventory/0")
    assert result.status_code == 204
    
    #  Check delete on invalid ID
    result = test_client.delete("/inventory/420")
    assert result.status_code == 404