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
    #  Add valid item
    new_item = Item("Cereal", "000", 1)
    inventory.add(new_item)
    assert new_item in inventory.get()
    
    #  Add items of wrong types
    with pytest.raises(TypeError):
        inventory.add(None)
        inventory.add("I am not of type Item")

def test_get(inventory):
    """Test that get returns the whole list, or specific index."""
    assert type(inventory.get()) == list
    first_id = inventory.get()[0].id
    assert type(inventory.get(first_id)) == Item
    with pytest.raises(ValueError):
        inventory.get("420")
    
def test_update_item(inventory):
    """Tests that existing item is updated."""
    #  If item doesn't exist, raise ValueError
    with pytest.raises(ValueError):
        inventory.update(id="1984", name="Corn")
    #  If item is updated, it is in list, and old item is not
    first_item = inventory.get()[0]
    old_name = first_item.name
    new_item_kwargs = {
        "name": "Resee's Puffs", 
        "barcode": "001", 
        "quantity": 3
    }
    inventory.update(first_item.id, **new_item_kwargs)
    assert old_name not in first_item.name
    assert all(str(item) in str(first_item) for item in new_item_kwargs.values())

def test_delete_item(inventory):
    """Tests that an existing item is deleted."""
    #  If item doesn't exist, raise ValueError
    with pytest.raises(ValueError):
        inventory.delete(id="420")
    #  If item is deleted, it is not in list
    #    Check item by id
    item_to_delete = inventory.get()[0]
    inventory.delete(item_to_delete.id)
    assert item_to_delete not in inventory.get()