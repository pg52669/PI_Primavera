"""
Events System Backend - Main Application
"""

from flask import Flask
from db_init import init_database
from routes import register_routes

# Create Flask application
app = Flask(__name__)

# Register all route blueprints
register_routes(app)


if __name__ == "__main__":
    # Initialize database tables
    init_database()
    # Run the Flask application
    print(
        "🚀 Starting Events API on http://0.0.0.0:5000 (accessible on host at http://localhost:5001)"
    )
    app.run(host="0.0.0.0", port=5000, debug=True)
