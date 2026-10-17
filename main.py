"""
Contains the CLI program that will call fetches on app.py
"""

from src.inventory import Item, Inventory
import src.api as api
import requests

def select_item(items: list[Item]) -> Item | None:
    """Prints all items in the inventory provided.
    Prompts selection of a specific item."""
    #  TODO response = requests.get
    #  TODO raise for status
    #  TODO json dumps list of Items
    #  TODO print items
    #  TODO show selection prompt
        #  TODO if exit, return None
    #  TODO validate selection and return Item
    pass

def add_item() -> None:
    """Prompts for input to search API by name or barcode.
    Posts new item to server."""
    #  TODO prompt search by name or barcode?
    #  TODO save barcode and name as blank placeholders, so that
    #    if manual entry fallback is used, the fields used are pre-populated
    #  TODO manual entry fallback function
    #  TRY the fetches; if runtime 503, offer manual entry instead
    #  IF BARCODE:
        #  TODO validate barcode format
        #  TODO fetch from API
        #  TODO print result, confirm accuracy
        #  TODO set barcode, name, and brand based on result
    #  IF NAME:
        #  TODO validate name is valid string
        #  TODO fetch search results from API
        #  TODO for top 3 results, print name and brand
        #  TODO select 1-3 or exit
        #  TODO set barcode, name, and brand based on results
    #  EXCEPT runtimeerror: manual entry fallback
    #  TODO input quantity
    #  TODO requests.post item
    #  TODO return to main menu

def update_item() -> None:
    """Update an existing item."""
    #  TODO call select_item, if returns none, return to main menu
    #  TODO print instructions
    #  TODO input new name
        #  IF blank, use existing name
    #  TODO input new brand
        #  IF blank, use existing brand
    #  TODO input new quant
        #  IF blank, use existing quant
    #  TODO confirm new item's information, or exit to menu
    #  TODO requests.patch item
    #  TODO return to main menu

def delete_item() -> None:
    """Delete an existing item."""
    #  TODO call select_item, if returns None, return to main menu
    #  TODO confirm deletion or exit
    #  TODO requests.delete item
    #  TODO return to main menu

def main():
    pass