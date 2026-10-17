"""
Contains the CLI program that will call fetches on app.py
"""

from src.inventory import Item, Inventory
import src.api as api
from src.app import create_app
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
        print(f"{index+1}. {item["name"]} - Brand: {item["brand"]} - Quantity: {item["quantity"]} - Barcode: {item["barcode"]}")
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
        selection = input("> ")
        
        #  Check blank response or "exit"
        if not selection or not selection.strip():
            print("Input cannot be empty.")
            continue
        if selection.lower() == "exit":
            return None
        
        #  Validate index into items list
        try:
            index = int(selection.strip()) - 1
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
                print(f"{updated_item["name"]} - Brand: {updated_item["brand"]} - Quantity: {updated_item["quantity"]}\n")
                print("Is this correct? Type 'yes' to confirm, or 'no' to try again. Type 'exit' to return to menu.")
            
                confirmation = input("> ")
                if not confirmation or not confirmation.strip():
                    print("Input must be 'yes', 'no', or 'exit'.")
                    continue
                
                #  "yes" returns True, "no" returns False, "exit" returns None
                match confirmation.lower():
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
    #  TODO call select_item, if returns None, return to main menu
    #  TODO confirm deletion or exit
    #  TODO requests.delete item
    #  TODO return to main menu
    pass


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
        running = False  # ensures loop never starts

    #  Main loop
    while running:
        #  Main input
        print(
            "Please select from the following options: list, add, update, delete, exit"
        )
        command = input("> ")

        #  Check if command is empty
        if not input or not input.strip():
            print("Command input cannot be blank.")
            continue

        #  Switch based on command chosen
        #  Wrapped in a try/except block to neatly exit in the case of errors
        try:
            match command.lower():
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
            print(f"The program encountered a fatal error: {err}")
            running = False


if __name__ == "__main__":
    create_app().run()  # Create and run Flask app
    main()
