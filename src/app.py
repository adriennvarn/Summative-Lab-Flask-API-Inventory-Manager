"""
Contains flask routing that will safely update db contained in inventory.py
"""

from flask import Flask, jsonify, request

#  App object that holds all routing information
def create_app():
    app = Flask(__name__)

    @app.get("/api/health")
    def health_check():
        """Health check to ensure server is running."""
        return jsonify({"status": "ok"})
    
    return app

#  Create app object
app = create_app()

if __name__ == "__main__":
    app.run()