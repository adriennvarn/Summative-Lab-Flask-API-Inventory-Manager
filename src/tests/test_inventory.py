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
    assert type(inventory.get(0)) == Item
    with pytest.raises(ValueError):
        inventory.get(420)
    with pytest.raises(TypeError):
        inventory.get("0")
    
def test_update_item(inventory):
    """Tests that existing item is updated."""
    #  If item doesn't exist, raise ValueError
    with pytest.raises(ValueError):
        inventory.update(index=69, name="Corn")
    #  If item is updated, it is in list, and old item is not
    old_item = Item("Cereal", "000", 1)
    new_item_kwargs = {
        "name": "Resee's Puffs", 
        "barcode": "001", 
        "quantity": 3
    }
    inventory.update(index=0, **new_item_kwargs)
    assert old_item not in inventory.get()
    assert Item(**new_item_kwargs) in inventory.get()

def test_delete_item(inventory):
    """Tests that an existing item is deleted."""
    #  If item doesn't exist, raise ValueError
    with pytest.raises(ValueError):
        inventory.delete(index=420)
    #  If item is deleted, it is not in list
    #    Check item by Item object
    item_to_delete = Item("Yogurt", "333", 2)
    inventory.add(item_to_delete)
    inventory.delete(item=item_to_delete)
    assert item_to_delete not in inventory.get()
    #    Check item by index
    indexed_item = inventory.get(0)
    inventory.delete(index=0)
    assert indexed_item not in inventory.get()