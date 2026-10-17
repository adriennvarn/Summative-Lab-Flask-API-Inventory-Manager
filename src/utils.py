"""Miscellaneous utility functions, primarily used by the CLI to verify inputs."""

def prompt_text(keep_case=False) -> str | None:
    """Prompts for input and returns a clean string.
    Returns:
        str: stripped lowercase string of user input
        None: if input is invalid in any way"""
    
    response = input("> ")
    
    if not response or not isinstance(response, str) or not response.strip():
        return None
    else:
        if keep_case:
            return response.strip()
        return response.strip().lower()

def item_as_string(item: dict) -> str:
    return f"{item['name']} - Brand: {item['brand']} - Quantity: {item['quantity']} - Barcode: {item['barcode']}"