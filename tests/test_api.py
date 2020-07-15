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

@pytest.fixture
def poll_data():
    data = {
        'poll_description': 'This is the question',
        'options': ['First Option', 'Second Option', 'Third Option']
    }

    return data

def test_post_poll(client, poll_data):
    """Check when creating a poll."""

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
    response = client.post('/poll', json=poll_data)
    assert response.status_code == 201
    assert response.is_json
    assert 'poll_id' in response.json

def test_get_poll(client, poll_data):
    """Check when finding a poll."""

    # Responds 404 when not found
    response = client.get('/poll/1')
    assert response.status_code == 404
    assert response.get_data(as_text=True) == 'Poll was not found\n'

    # Responds 200 with a JSON when found
    client.post('/poll', json=poll_data)
    response = client.get('/poll/1')
    assert response.status_code == 200
    assert response.is_json

    # Check JSON structure
    json = response.json
    assert 'poll_id' in json
    assert 'poll_description' in json
    assert 'options' in json
    assert type(json['options']) is list

def test_stats_poll(client, poll_data):
    """Check when requesting stats."""

    # Responds 404 when not found
    response = client.get('/poll/1/stats')
    assert response.status_code == 404
    assert response.get_data(as_text=True) == 'Poll was not found\n'

    # Post a poll for tests
    client.post('/poll', json=poll_data)

    # Responds 200 with a JSON when found
    response = client.get('poll/1/stats')
    assert response.status_code == 200
    assert response.is_json

    json = response.json
    assert 'views' in json
    assert json['views'] == 0
    assert 'votes' in json
    assert type(json['votes']) is list

    # Check if views increases with each `GET /poll/:poll_id`
    client.get('poll/1')
    response = client.get('poll/1/stats')
    assert response.status_code == 200
    assert response.is_json
    assert response.json['views'] == 1

def test_vote_option(client, poll_data):
    """Check when registering a vote."""

    # Responds 404 when not found
    response = client.post('/poll/1/vote')
    assert response.status_code == 404
    assert response.get_data(as_text=True) == 'Poll option was not found\n'

    # Post a poll for tests
    client.post('/poll', json=poll_data)
    response = client.get('poll/1/stats')
    assert response.status_code == 200
    assert 'votes' in response.json

    option = response.json['votes'][0]
    assert option['qty'] == 0

    # Successfully post a vote
    response = client.post('/poll/1/vote')
    assert response.status_code == 200
    assert response.is_json
    assert 'option_id' in response.json

    # Check if option is increased by 1
    response = client.get('poll/1/stats')
    assert response.status_code == 200
    assert 'votes' in response.json

    option = response.json['votes'][0]
    assert option['qty'] == 1
