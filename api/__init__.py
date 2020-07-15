from flask import Flask

SQLALCHEMY_DATABASE_URL = 'sqlite:///./database.db'

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(DATABASE=SQLALCHEMY_DATABASE_URL)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # Register the database commands
    from api.database import init_app
    init_app(app)

    # Apply the blueprints to the app
    from api.controllers import poll_controller
    app.register_blueprint(poll_controller.bp)

    return app
