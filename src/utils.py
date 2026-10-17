"""Miscellaneous utility functions, primarily used by the CLI to verify inputs."""

def prompt_text() -> str | None:
    """Prompts for input and returns a stripped lowercase string of input."""
    
    response = input("> ")
    
    if not response or not isinstance(response, str) or not response.strip():
        return None
    else:
        return response.strip().lower()

def item_as_string(item: dict) -> str:
    return f"{item["name"]} - Brand: {item["brand"]} - Quantity: {item["quantity"]} - Barcode: {item["barcode"]}"