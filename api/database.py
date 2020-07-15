import click
from flask import current_app, g
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def get_db():
    """Connect to the application's configured database."""

    if 'db_session' not in g:
        engine = create_engine(current_app.config['DATABASE'], connect_args={'check_same_thread': False})
        db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

        Base.query = db_session.query_property()

        g.engine = engine
        g.db_session = db_session

    return g.db_session

def init_db():
    """Clear existing data and create new tables."""

    get_db()

    from api.models import poll, poll_option

    Base.metadata.drop_all(bind=g.engine)
    Base.metadata.create_all(bind=g.engine)

def close_db(e=None):
    """Shutdown the session."""

    db_session = g.pop('db_session', None)

    if db_session is not None:
        db_session.remove()

@click.command('init_db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""

    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """Register database functions with the Flask app."""

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
