from unittest.mock import patch
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
    fake_item = {
            "id": "abc",
            "name": "Cereal",
            "barcode": "000",
            "brand": "General Mills",
            "quantity": 1,
        }
    
    with patch("src.inventory.Inventory.get") as mock_get:
        mock_get.return_value = fake_item

        #  Call get
        result = test_client.get("/inventory/abc")
        #  Verify data
        assert result.status_code == 200
        assert result.get_json() == fake_item

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
        json={"name": "Cereal", "barcode": "000", "brand": "General Mills", "quantity": 1},
    )
    assert result.status_code == 201
    
    #  Call with invalid JSONs
    result = test_client.post(
        "/inventory",
        json={"barcode": "000", "brand": "General Mills", "quantity": 1},
    )  # No name
    assert result.status_code == 400
    
    result = test_client.post(
        "/inventory",
        json={"name": "Cereal", "brand": "General Mills", "quantity": 1},
    )  # No barcode
    assert result.status_code == 400
    
    result = test_client.post(
        "/inventory",
        json={"name": "Cereal", "barcode": "000", "brand": "General Mills"},
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
    fake_item = {
            "id": "0",
            "name": "Resee's Puffs",
            "barcode": "000",
            "brand": "General Mills",
            "quantity": 1,
        }
    
    update_json = {"name": "Resee's Puffs"}
    responses.add(responses.PATCH, f"{BASE_URL}/0", json=fake_item.update(update_json), status=200)
    result = test_client.patch("/inventory/0", json=update_json)
    assert result.status_code == 200
    assert result.get_json()["name"] == "Resee's Puffs"
    
    #  Check patch with invalid JSON or ID
    result = test_client.patch("/inventory/0", json={})
    assert result.status_code == 400
    
    result = test_client.patch("/inventory/420", json={"name": "Fake Item"})
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