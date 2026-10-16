"""
Contains inventory db and methods to safely update it
Allows changing of internal data management without updating flask methods
"""

from uuid import uuid4 as uuid


class Item:
    def __init__(self, name: str, barcode: str, quantity: int, brand: str = "Unknown"):
        self.id = str(uuid())
        self.name = name
        self.barcode = barcode
        self.brand = brand
        self.quantity = quantity

    def __str__(self):
        return f"""Name: {self.name}
    Barcode: {self.barcode}
    Brand: {self.brand}
    Quantity: {self.quantity}"""

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def barcode(self):
        return self._barcode

    @barcode.setter
    def barcode(self, value: str):
        if not value:
            raise ValueError("Barcode cannot be empty.")
        if not value.strip().isdigit():
            raise ValueError("Barcode can only contain numbers.")
        self._barcode = value

    @property
    def brand(self):
        return self._brand

    @brand.setter
    def brand(self, value: str):
        if not value or not value.strip():
            self._brand = "Unknown"
        else:
            self._brand = value

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        if not value:
            raise ValueError("Quantity must not be blank.")
        if value <= 0:
            raise ValueError("Quantity must be a positive number.")
        self._quantity = value


class Inventory:
    __inventory = []

    @classmethod
    def get(cls, id: str = None):
        #  If no ID specified, return all
        if not id:
            return cls.__inventory.copy()
        #  Check if ID exists; if yes, return it
        item = next((item for item in cls.__inventory if item.id == id), None)
        if not item:
            raise ValueError(f"No item with ID {id} was found.")
        return item

    @classmethod
    def add(cls, value: Item):
        if not value:
            raise TypeError("Cannot add empty item to inventory.")
        if type(value) is not Item:
            raise TypeError(
                f"Inventory.add expected type Item, received type {type(value)}"
            )
        cls.__inventory.append(value)

    @classmethod
    def update(cls, index: int, name=None, barcode=None, brand=None, quantity=None):
        if not 0 <= index < len(cls.__inventory):
            raise IndexError("Index must be within bounds of Inventory array.")
        item: Item = cls.__inventory[index]
        if name:
            item.name = name
        if barcode:
            item.barcode = barcode
        if brand:
            item.brand = brand
        if quantity:
            item.quantity = quantity

    @classmethod
    def delete(cls, index: int):
        if index == None:
            raise ValueError("Must specify the index of item to delete.")
        if not 0 <= index < len(cls.__inventory):
            raise IndexError("Index must be within bounds of Inventory array.")
        cls.__inventory.pop(index)
