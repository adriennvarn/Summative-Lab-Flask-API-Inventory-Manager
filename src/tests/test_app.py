import pytest

def test_health_check():
    """GIVEN a Flask application configured for testing
    WHEN the "/api/health" page is requested via GET
    THEN check that the status is valid"""
    #  TODO
    pass

def test_get_inventory(test_client):
    """GIVEN a Flask application configured for testing
    WHEN the "/inventory" page is requested via GET
    THEN check that a list of Item objects is returned"""
    #  TODO
    pass

def test_get_by_id(test_client):
    """GIVEN a Flask app and an ID number
    WHEN the "/inventory/id/" page is requested via GET
    THEN check that a single Item object is returned"""
    #  TODO
    pass

def test_post_item(test_client):
    """GIVEN a Flask app and a new Item object
    WHEN the "/inventory" page is POSTed to
    THEN check that:
        - A 201 response is generated on valid JSON
        - A 400 response is generated on invalid JSON"""
    #  TODO
    pass

def test_patch_item(test_client):
    """GIVEN a Flask app and an existing Item object
    WHEN the "/inventory/id/" page is PATCHed
    THEN check that:
        - A 200 response is generated on successful patch
        - A 400 response is generated on invalid JSON
        - A 404 response is generated on non-existing ID"""
    #  TODO
    pass

def test_delete_item(test_client):
    """GIVEN a Flask app and an existing Item object
    WHEN the "/inventory/id/" page is DELETEd
    THEN check that:
        - A 204 response is generated on successful patch
        - A 404 response is generated on non-existing ID"""
    #  TODO
    pass