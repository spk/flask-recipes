import json
import pytest
from app import create_app
from app.extensions import db
from app.models import Recipe, Category
from app.tasks import import_recipe


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app()
    app.config['TESTING'] = True

    # create the database and load test data
    with app.app_context():
        db.create_all()
        db.session.begin(subtransactions=True)

    yield app

    with app.app_context():
        db.session.rollback()
        db.session.close()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def test_import_recipe_success(app, client):
    import_recipe("""<?xml version="1.0" encoding="UTF-8"?>
<recipeml version="0.5">
<recipe>
<head><title>test</title><categories><cat>Vegetarian</cat></categories></head>
</recipe>
</recipeml>""")
    with app.app_context():
        assert db.session.query(Recipe).filter_by(
            title="test").first().title == "test"
        assert db.session.query(Category).filter_by(
            title="Vegetarian").first().title == "Vegetarian"


def test_import_recipe_parse_error(app, client):
    import_recipe("""<?xml version="1.0" encoding="UTF-8"?>
<recipeml version="0.5"><recipe><head><title>test</title></head></recipe>""")
    with app.app_context():
        assert db.session.query(Recipe).filter_by(title="test").first() is None


def test_import_recipe_with_slash(app, client):
    with app.app_context():
        category = Category(title='Vegetarian')
        db.session.add(category)
        db.session.commit()
    import_recipe("""<?xml version="1.0" encoding="UTF-8"?>
<recipeml version="0.5">
<recipe>
<head><title>test</title><categories><cat>Vegetarian/</cat></categories></head>
</recipe>
</recipeml>""")
    with app.app_context():
        assert db.session.query(Recipe).filter_by(
            title="test").first().title == "test"
        assert db.session.query(Category).filter_by(
            title="Vegetarian").first().title == "Vegetarian"


def test_empty_db(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert 'No entries.'.encode('utf-8') in rv.data


def test_random_with_no_data(client):
    assert client.get('/random').status_code == 404


def test_random_with_data(app, client):
    title = 'random'
    with app.app_context():
        new_recipe = Recipe(title=title)
        db.session.add(new_recipe)
        db.session.commit()

    rv = client.get('/random')
    assert rv.status_code == 200
    assert title.encode('utf-8') in rv.data


def test_recipes_with_quantity(app, client):
    title = 'with_quantity'
    quantity = 1
    with app.app_context():
        new_recipe = Recipe(title=title, quantity=quantity)
        db.session.add(new_recipe)
        db.session.commit()
        rv = client.get('/{0}'.format(new_recipe.id))
        h1 = '{0} ({1})'.format(title, quantity)
        assert h1.encode('utf-8') in rv.data


def test_recipes_without_quantity(app, client):
    title = 'without_quantity'
    quantity = None
    with app.app_context():
        new_recipe = Recipe(title=title, quantity=quantity)
        db.session.add(new_recipe)
        db.session.commit()
        rv = client.get('/{0}'.format(new_recipe.id))
        h1 = '{0}'.format(title)
        assert h1.encode('utf-8') in rv.data


def test_no_categories(client):
    rv = client.get('/categories/')
    assert 'No entries.'.encode('utf-8') in rv.data


def test_with_categories(app, client):
    with app.app_context():
        category = Category(title='Vegetarian')
        db.session.add(category)
        db.session.commit()
        rv = client.get('/categories/')
        assert category.title.encode('utf-8') in rv.data


def test_recipes_without_categories(client):
    with client as c:
        rv = c.get('/categories/None')
        assert rv.status_code == 404


def test_recipes_with_categories(app, client):
    title = 'category'
    with app.app_context():
        category = Category(title=title)
        db.session.add(category)
        db.session.commit()
        new_recipe = Recipe(title='title', quantity=10, categories=[category])
        db.session.add(new_recipe)
        db.session.commit()
        rv = client.get('/categories/{0}'.format(title))
        assert rv.status_code == 200


def test_api_get_recipe(app, client):
    title = 'json'
    with app.app_context():
        new_recipe = Recipe(title=title)
        db.session.add(new_recipe)
        db.session.commit()
        rv = client.get('/api/v1/{0}'.format(new_recipe.id))
        data = json.loads(rv.data)
        assert data['title'] == title


def test_api_get_recipes(app, client):
    title = 'recipes api'
    with app.app_context():
        new_recipe = Recipe(title=title)
        db.session.add(new_recipe)
        db.session.commit()
        rv = client.get('/api/v1/recipes')
        data = json.loads(rv.data)
        assert data['has_next'] is False
        assert data['has_prev'] is False
        assert new_recipe.title == data['items'][0]['title']
        assert data['page'] == 1
        assert data['pages'] == 1
        assert data['per_page'] == 10
        assert data['total'] == 1


def test_clean_title_before_insert(app, client):
    title = 'test /'
    with app.app_context():
        new_recipe = Recipe(title=title)
        db.session.add(new_recipe)
        db.session.commit()
        assert new_recipe.title == 'test'
