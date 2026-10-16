"""
Contains flask routing that will safely update db contained in inventory.py
"""

from flask import Flask, jsonify, request
from src.inventory import Inventory

#  App object that holds all routing information
def create_app():
    app = Flask(__name__)

    @app.get("/api/health")
    def health_check():
        """Health check to ensure server is running."""
        return jsonify({"status": "ok"})
    
    @app.get("/inventory")
    def get_all():
        """Return all inventory items."""
        return jsonify(Inventory.get()), 200
    
    @app.get("/inventory/<string:id>")
    def get_by_id(id):
        try:
            return jsonify(Inventory.get(id)), 200
        except ValueError as err:
            return jsonify(err), 404
    
    return app

#  Create app object
app = create_app()

if __name__ == "__main__":
    app.run()