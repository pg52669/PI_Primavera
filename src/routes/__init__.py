"""
Routes package - Flask route handlers (thin controllers)
"""

from .event_routes import events_api
from .user_routes import users_api
from .organisation_routes import organisations_api
from .location_routes import locations_api


def register_routes(app):
    """Register all route blueprints with the Flask app"""
    app.register_blueprint(events_api)
    app.register_blueprint(users_api)
    app.register_blueprint(organisations_api)
    app.register_blueprint(locations_api)


__all__ = ["register_routes"]
