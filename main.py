"""
Contains the CLI program that will call fetches on app.py
"""

from src.inventory import Item, Inventory
import src.api as api
from src.app import create_app
from src.utils import *
import requests

BASE_URL = "http://localhost:5000/inventory"


def list_items() -> list[dict] | None:
    """Prints a list of all items in the current inventory, and returns it."""
    
    #  Get response from server
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"The Flask server encountered an error: {err}")
        return None
    
    #  Get data as a list of dicts
    data = response.json()
    
    if not data:
        print(f"Your inventory is empty. Add some items first!\n")
        return None
    
    #  Print all items in list
    for index, item in enumerate(data):
        print(f"{index+1}. {item_as_string(item)}")
    #  Return if calling function requires the list
    return data


def select_item() -> dict | None:
    """Prints all items in the inventory provided.
    Prompts selection of a specific item."""
    
    items = list_items()
    #  If items is None, inventory was empty (or err) and it was handled already.
    if not items:
        return None
    
    #  Continue prompting until valid response
    prompting = True
    while prompting:
        print(f"Please select an item from the list by entering a number 1-{len(items)}, or exit.")
        selection = prompt_text()
        
        #  Check blank response or "exit"
        if not selection:
            print("Input cannot be empty.")
            continue
        if selection == "exit":
            return None
        
        #  Validate index into items list
        try:
            index = int(selection) - 1
            #  Return item as dict
            return items[index]
        except:  # Handle ValueError if index cannot map to int, or IndexError if index out of range
            print(f"Must enter a valid number between 1 and {len(items)}, or exit.")
            continue
    
    #  Fallback if no return statement reached
    raise RuntimeError("No return statement reached in main.select_item")
        


def add_item() -> None:
    """Prompts for input to search API by name or barcode.
    Posts new item to server."""
    
    
    #  TODO prompt search by name or barcode?
    #  TODO save barcode and name as blank placeholders, so that
    #    if manual entry fallback is used, the fields used are pre-populated
    
    #  Looping main prompt to establish which search function to use
    main_prompt = True
    while main_prompt:
        print("Would you like to search for an item by name or barcode?")
        print("Enter 'name', 'barcode', or 'exit'.")
        search_mode = prompt_text()
        
        if not search_mode:
            print("Please select a field to search by.")
            continue
        
        match search_mode:
            case "name":
                pass
            case "barcode":
                pass
            case "exit":
                print("Returning to menu.")
                return
    
    def manual_entry(name=None, barcode=None) -> dict | None:
        """Prompts if the user wants to use manual entry,
        and returns an item built from manually entered information.
        Returns:
            item (dict): manually entered item
            None: if user refuses or cancels entry"""
        
        while True:
            print("Would you like to enter information manually? Type 'yes', 'no', or 'cancel'.")
            manual = prompt_text()
            #  Handle blank input and cancel
            if not manual:
                print("Response cannot be blank.")
                continue
            match manual:
                case "no" | "cancel":
                    return None
                case "yes":  # break out of prompt loop and proceed
                    break
                case _:
                    print("Invalid response.")
                    continue
        
    def search_by_name() -> dict | None:
        """Search API by name. Returns a dict of useful fields if successful,
        raises error if no result found / API error,
        or returns None if user exits."""
        
        while True:
            print("Please enter the name of the item you're looking for, or 'cancel' to return to add menu.")
            name = prompt_text()
            
            if not name:
                print("Entry cannot be blank.")
                continue
            if name == "cancel":
                return None
            #  Assume name entry is valid and proceed
            break
            
        try:
            products = api.get_products_by_name(name)
            print("Here are the results: ")
            for index, product in enumerate(products):
                print(f"{index+1}. Name: {product["name"]} - Brand: {product["brand"]} - Barcode: {product["barcode"]}")
            
            while True:
                print("Which item would you like to add? Enter it's number, or 'cancel' to return to add menu.")
                selection = prompt_text()
                #  Handle blank input and cancel
                if not selection:
                    print("Selection cannot be blank.")
                    continue
                if selection == "cancel":
                    return None
                #  Attempt to get index from selection
                try:
                    index = int(selection)
                except ValueError:
                    print(f"Input must be a number between 1 and {len(products)}, or 'cancel'.")
                    continue
                #  Assume index is valid and return selected product
                return products[index]
        except RuntimeError:
            print("It looks like the search API isn't available right now.")
            #  Ask if user wants to use manual entry
            return manual_entry(name=name)
            
            
    
    #  IF NAME:
    #  TODO validate name is valid string
    #  TODO fetch search results from API
    #  TODO for top 3 results, print name and brand
    #  TODO select 1-3 or exit
    #  TODO set barcode, name, and brand based on results
    
    
    
    #  TODO manual entry fallback function
    
    #  TRY the fetches; if runtime 503, offer manual entry instead
    
    #  IF BARCODE:
    #  TODO validate barcode format
    #  TODO fetch from API
    #  TODO print result, confirm accuracy
    #  TODO set barcode, name, and brand based on result
    
    
    #  EXCEPT runtimeerror: manual entry fallback
    
    
    #  TODO input quantity
    #  TODO requests.post item
    #  TODO return to main menu
    pass


def update_item() -> None:
    """Update an existing item."""    
    #  List items and get selection
    item = select_item()
    
    #  Loop to retry update if final confirmation is rejected
    prompting = True
    while prompting:
        #  Print instructions
        print("For each field, enter a new value, or leave blank to keep existing value.")
        
        #  New values, which are set to None if unchanged
        new_name = input(f"Name (currently {item["name"]}): ")
        new_brand = input(f"Brand (currently {item["brand"]}): ")
        new_quantity = input(f"Quantity (currently {item["quantity"]}): ")
        
        #  Clean any empty or whitespace strings to None
        for field in [new_name, new_brand, new_quantity]:
            if not field or not field.strip():
                field = None
        
        #  Convert quantity to int, if provided, as that's what Item expects
        try:
            if new_quantity:
                new_quantity = int(new_quantity.strip())
        except ValueError:
            print("Quantity must be a valid integer. Please try again.")
            continue
        
        #  Create updated item safely
        updated_item = item
        if new_name:
            updated_item["name"] = new_name
        if new_brand:
            updated_item["brand"] = new_brand
        if new_quantity:
            updated_item["quantity"] = new_quantity
        
        #  Utility function that will loop until a valid confirmation is received
        def is_confirmed(item: dict) -> bool | None:
            #  Loop on confirmation prompt. This is so that, if an invalid input is provided,
            #    the user doesn't have to repeat the entire process.
            confirm_prompting = True
            while confirm_prompting:
                print("Updated Item:\n")
                print(item_as_string(updated_item))
                print("Is this correct? Type 'yes' to confirm, or 'no' to try again. Type 'exit' to return to menu.")
            
                confirmation = prompt_text()
                if not confirmation:
                    print("Input must be 'yes', 'no', or 'exit'.")
                    continue
                
                #  "yes" returns True, "no" returns False, "exit" returns None
                match confirmation:
                    case "yes":
                        return True
                    case "no":  # break out of function loop without breaking out of outer loop
                        confirm_prompting = False
                        return False
                    case "exit":
                        print("Item not updated.\n")
                        return None
                    case _:
                        print("Input must be 'yes', 'no', or 'exit'.")
                        continue
        
        #  Use utility function to check for confirmation and PATCH if so
        match is_confirmed(updated_item):
            case None:  # "exit" jumps out of update function
                return
            case False:  # User wants to try again
                continue
            case True:  # PATCH item
                try:
                    response = requests.patch(f"{BASE_URL}/{item["id"]}", json=updated_item)
                    response.raise_for_status()
                    print("Item updated successfully!")
                except requests.exceptions.HTTPError as err:
                    print(f"The Flask server encountered an error: {err}")
                    
                return  # PATCH either succeeded or failed, either way, return


def delete_item() -> None:
    """Delete an existing item."""
    
    #  List items and get selection
    item = select_item()
    
    #  Loop until valid confirmation response
    prompting = True
    while prompting:
        print("You selected:")
        print(item_as_string(item))
        print("Are you sure you want to delete this item? Enter 'yes' to delete, 'no' to preserve, or 'exit' to return to menu.")
        confirmation = prompt_text()
        
        #  Validate confirmation isn't blank and switch on it
        if not confirmation:
            print("Please enter 'yes', 'no', or 'exit'.")
            continue
        match confirmation:
            case "yes":
                try:  # call delete, print confirmation on success
                    response = requests.delete(f"{BASE_URL}/{item["id"]}")
                    response.raise_for_status()
                    print("Item deleted successfully.\n")
                except requests.exceptions.HTTPError as err:
                    print(f"The Flask server encountered an error: {err}")
            case "no"|"exit":
                print("Returning to menu...\n")
                return
            

def main() -> None:
    print("\nWelcome to Inventory Manager!\n")

    #  Main loop control
    running = True

    #  Verify Flask server is running
    response = requests.get("http://localhost:5000/api/health")
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("The Flask server doesn't appear to be running.")
        print(f"Error: {err}")
        return  # exits program immediately

    #  Main loop
    while running:
        #  Main input
        print(
            "Please select from the following options: list, add, update, delete, exit"
        )
        command = prompt_text()

        #  Check if command is empty
        if not command:
            print("Command input cannot be blank.")
            continue

        #  Switch based on command chosen
        #  Wrapped in a try/except block to neatly exit in case of uncaught errors
        try:
            match command:
                case "list":
                    list_items()
                case "add":
                    add_item()
                case "update":
                    update_item()
                case "delete":
                    delete_item()
                case "exit":
                    print("\nThanks for using this app! Goodbye!\n")
                    running = False
                    continue
                case _:
                    print("Invalid command entered.")
        except Exception as err:
            print(f"The program encountered an unknown error: {err}")
            running = False


if __name__ == "__main__":
    create_app().run()  # Create and run Flask app
    main()
