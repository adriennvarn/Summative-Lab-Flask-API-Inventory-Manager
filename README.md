# API Inventory Manager
### By Adrienn Varn
Inventory Manager CLI tool using a Flask API, for Flatiron School SE-FND2-FT Module 16 Summative Assessment

## Features
- Interactive CLI to manage inventory
- Flask interface that allows management of inventory through any HTTP tool.
- Database persists as long as Flask is running; the CLI can be closed and reopened as many times as you want.

## Requirements
- Python 3.10+ (I built this with 3.11)
- pipenv
- A terminal application

## Installation
Fork and clone GitHub repo.

Inside git folder, run `pipenv install`. Optionally, specify Python version installed on your computer. For example, I use `pipenv install --python 3.11`.

You will need two terminals, or a session manager like screen or tmux. You have two choices for running the applications: in each terminal, run `pipenv shell` before executing each command, or preface each command with `pipenv run` (without pressing enter). If you use the shell, you may have to type both `deactivate` and `exit` to escape pipenv; I've had very inconsistent results with this.

In the first terminal, move to the src folder and run `flask run`. This will start the Flask HTTP server.

In the second terminal, run `python3 main.py`. This opens the CLI application.

## Usage
Every input is given clear instructions. You can cancel or exit from every input.

When the app starts, you can view your inventory, add to it, update an item on it, or delete an item.

When adding items, the API at [OpenFoodFacts](https://openfoodfacts.org) is used to look up an item's information by either a name search, or it's UPC code (barcode).

**Note on API**: it is very unreliable and prone to 'service unavailable' errors, which are the fault of the servers and not this application. The program will display a message that the API is unavailable and prompt you for manual entry. 
