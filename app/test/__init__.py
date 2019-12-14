import pytest
from app.extensions import db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app()
    app.config['TESTING'] = True

    # create the database and load test data
    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def create_recipe(db, **kwargs):
    new_recipe = Recipe(**kwargs)
    db.session.add(new_recipe)
    db.session.commit()
    return new_recipe
