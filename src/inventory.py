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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "barcode": self.barcode,
            "brand": self.brand,
            "quantity": self.quantity,
        }

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
    def get(cls, id: str = None) -> list | Item :
        #  If no ID specified, return all
        if not id:
            return cls.__inventory.copy()
        #  Check if ID exists; if yes, return it
        item: Item = next((item for item in cls.__inventory if item.id == id), None)
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
    def update(cls, id: str, **kwargs):
        item: Item = next((item for item in cls.__inventory if id == item.id), None)
        if not item:
            raise ValueError(f"No item with ID {id} was found.")
        for key, value in kwargs.items():
            if hasattr(item, key):
                setattr(item, key, value)

    @classmethod
    def delete(cls, id: str):
        if id == None:
            raise ValueError("Must specify the ID of item to delete.")
        item: Item = next((item for item in cls.__inventory if id == item.id), None)
        if not item:
            raise ValueError(f"No item with ID {id} was found.")
        cls.__inventory.remove(item)
