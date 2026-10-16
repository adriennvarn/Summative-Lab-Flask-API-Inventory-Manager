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
            raise ValueError("Brand name cannot be empty.")
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

    