"""
Contains inventory db and methods to safely update it
Allows changing of internal data management without updating flask methods
"""
from uuid import uuid4 as uuid


class Item:
    def __init__(self, name:str, barcode:str, quantity:int, brand:str="Unknown"):
        self.id = str(uuid())
        self.name = name
        self.barcode = barcode
        self.brand = brand
        self.quantity = quantity

class Inventory:
    __inventory = []
    
