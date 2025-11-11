"""
Routes package - Flask route handlers (thin controllers)
"""

from .event_routes import events_api
from .user_routes import users_api
from .organisation_routes import organisations_api
from .location_routes import locations_api
from .health_routes import health_api
from .volunteer_routes import volunteer_api
from .transport_routes import transport_api
from .message_routes import message_api


def register_routes(app):
    """Register all route blueprints with the Flask app"""
    app.register_blueprint(events_api)
    app.register_blueprint(users_api)
    app.register_blueprint(organisations_api)
    app.register_blueprint(locations_api)
    app.register_blueprint(health_api)
    app.register_blueprint(volunteer_api)
    app.register_blueprint(transport_api)
    app.register_blueprint(message_api)


__all__ = ["register_routes"]
