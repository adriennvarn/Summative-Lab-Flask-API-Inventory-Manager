import pytest
from src.inventory import Inventory, Item
from src.app import create_app

@pytest.fixture(scope="module")
def inventory():
    """Module scoped inventory object"""
    inventory = Inventory()
    return inventory

@pytest.fixture(scope="module")
def test_client():
    """Module scoped test client"""
    flask_app = create_app()
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client