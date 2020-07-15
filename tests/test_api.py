import pytest

from api import create_app
from api.database import init_db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""

    app = create_app({'TESTING': True, 'DATABASE': 'sqlite:///:memory:'})

    # create the database and load test data
    with app.app_context():
        init_db()
        yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_post_poll(client):
    """Check when creating a poll."""

    data = {
        'poll_description': 'This is the question',
        'options': ['First Option', 'Second Option', 'Third Option']
    }

    # Cannot create a poll without description
    response = client.post('/poll', json={})
    assert response.status_code == 400

    # Cannot create a poll without options
    response = client.post('poll', json={'poll_description': 'Title'})
    assert response.status_code == 400

    # Options must be an array
    response = client.post('poll', json={'poll_description': 'Title', 'options': 'test'})
    assert response.status_code == 400

    # Poll have been created
    response = client.post('/poll', json=data)
    assert response.status_code == 201
    assert response.is_json
    assert 'poll_id' in response.json
