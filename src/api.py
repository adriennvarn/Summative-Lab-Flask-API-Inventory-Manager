import requests


def get_products_by_name(name: str) -> list[dict[str, str]]:
    """
    Search Open Food Facts by product name and return list of best-matching barcodes.
    Raises:
        RuntimeError: if API request fails
    """

    url = "https://world.openfoodfacts.org/cgi/search.pl"

    #  Use a simple search to churn up the top 5 results to select from
    params = {
        "search_terms": name,
        "search_simple": "1",
        "action": "process",
        "json": "1",
        "page_size": "3",
    }

    #  Custom user agent headers required by API
    headers = {
        "User-Agent": "Flatiron Assessment - Version 0.1 - adriennvarn@gmail.com"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        products = data.get("products", [])
        if not products:
            raise ValueError(f"No results found for '{name}'")

        #  List of dictionaries providing info on top 5 results
        results = [
            {
                "name": product.get("product_name"),
                "brand": product.get("brands"),
                "barcode": product.get("code"),
            }
            for product in products
        ]

        return results
    #  Any exceptions are an upstream problem
    except Exception as err:
        raise RuntimeError(f"API Request failed: {err}")


def get_product(barcode: str) -> dict[str, str]:
    url = f"https://world.openfoodfacts.org/{barcode}.json"

    #  Custom user agent headers required by API
    headers = {
        "User-Agent": "Flatiron Assessment - Version 0.1 - adriennvarn@gmail.com"
    }

    #  Specify fields requested to optimize
    params = {"fields": "product_name,brands"}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == 1:  # 1 = product found
            product = data["product"]
            #  Return array of name and brand
            return {
                "name": product["product_name"],
                "brand": product["brands"],
            }
        else:
            raise ValueError("Product not found in database.")
    except RuntimeError as err:
        raise RuntimeError(f"API request failed: {err}")


# tests if run directly
if __name__ == "__main__":
    print("\n".join(get_products_by_name("Oreo double stuff")))
    print(get_product("3017624010701"))  # check with nutella's UPC