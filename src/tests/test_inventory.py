import pytest
from src.inventory import Item


def test_item_validation():
    """Tests validation of Item fields"""
    #  This will fail the test automatically if it raises anything.
    Item("Cereal", "000", 1)
    #  Assert failures of: blank name, blank barcode, quantity <= 0
    with pytest.raises(ValueError):
        Item("", "000", 1)
        Item("Cereal", "", 1)
        Item("Cereal", "000", -1)

def test_initializes_to_empty(inventory):
    """Test that new inventory object is empty."""
    assert inventory.get() == []

def test_add_item(inventory):
    """Test adding a valid or invalid item to inventory."""
    new_item = Item("Cereal", "000", 1)
    inventory.add(new_item)
    assert new_item in inventory.get()
    
    with pytest.raises(TypeError):
        inventory.add(None)
        inventory.add("I am not of type Item")
    
def test_update_item(inventory):
    """Tests that existing item is updated."""
    #  If item doesn't exist, raise ValueError
    #  If item is updated, it is in list, and old item is not
    #  TODO
    pass

def test_delete_item(inventory):
    """Tests that an existing item is deleted."""
    #  If item doesn't exist, raise ValueError
    #  If item is deleted, it is not in list
    #  TODO
    pass