from main import app, init
import pytest
import json


@pytest.fixture
def client():
    app.app.config['TESTING'] = True

    with app.app.test_client() as client:
        with app.app.app_context():
            init()
        yield client


def test_get_actors_10(client):
    rv = client.get('/api/v1/actor?limit=10&offset=2')
    assert rv.status_code == 200
    data_parsed = json.loads(rv.data)
    assert len(data_parsed) == 10


def test_get_actors_all(client):
    rv = client.get('/api/v1/actor')
    assert rv.status_code == 200
    data_parsed = json.loads(rv.data)
    assert len(data_parsed) == 196975


def test_bacon_number_0(client):
    rv = client.get('/api/v1/actor/Kevin Bacon/bacon_number')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert json_data.get('degrees', -1) == 0


def test_bacon_number_8(client):
    rv = client.get('/api/v1/actor/Mohammad Ali Barrati/bacon_number')
    assert rv.status_code == 200
    json_data = json.loads(rv.data)
    assert json_data.get('degrees', -1) == 8


def test_bacon_number_not_found(client):
    rv = client.get('/api/v1/actor/not found/bacon_number')
    assert rv.status_code == 404
