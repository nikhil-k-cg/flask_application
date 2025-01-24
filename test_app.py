import pytest
from app import app


@pytest.fixture
def client():
    """
    Creates a test client for your Flask app
    """
    with app.test_client() as client:
        yield client


def test_homepage(client):
    """
    Test the home page route
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to My Flask App" in response.data


def test_homepage_content(client):
    """
    Test that the home page contains specific content
    """
    response = client.get('/')
    assert b"This is a simple web application using Flask." in response.data
