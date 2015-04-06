import json
from unittest import TestCase as Base
from contextlib import contextmanager
from app.factory import create_app
from app.extensions import db
from app.models import Recipe, Category
from flask import url_for

class TestCase(Base):
    @classmethod
    def setUpClass(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        db.create_all()

    @classmethod
    def tearDownClass(self):
        db.session.remove()
        db.drop_all()

    def setUp(self):
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        db.session.begin(subtransactions=True)

    def tearDown(self):
        db.session.rollback()
        db.session.close()
        self._ctx.pop()

class AppTestCase(TestCase):
    def create_recipe(self, **kwargs):
        new_recipe = Recipe(**kwargs)
        db.session.add(new_recipe)
        db.session.commit()
        return new_recipe

    def test_empty_db(self):
        rv = self.client.get('/')
        assert 'No entries.' in rv.data

    def test_random_with_no_data(self):
        rv = self.client.get('/random')
        self.assertEqual(rv.status_code, 404)

    def test_random_with_data(self):
        recipe = self.create_recipe(title='random')
        rv = self.client.get('/random')
        self.assertEqual(rv.status_code, 200)
        assert recipe.title in rv.data

    def test_with_quantity(self):
        recipe = self.create_recipe(title='with quantity', quantity=1)
        rv = self.client.get('/{0}'.format(recipe.id))
        h1 = '{0} ({1})'.format(recipe.title, recipe.quantity)
        assert h1 in rv.data

    def test_without_quantity(self):
        recipe = self.create_recipe(title='without quantity', quantity=None)
        rv = self.client.get('/{0}'.format(recipe.id))
        h1 = '{0}'.format(recipe.title)
        assert h1 in rv.data

    def test_without_categories(self):
        with self.client as c:
            rv = c.get(url_for('recipes.categories', title='None'))
            self.assertEqual(rv.status_code, 404)

    def test_with_categories(self):
        title = 'category'
        categories = [Category(title=title)]
        recipe = self.create_recipe(title='title', quantity=10, categories=categories)
        with self.client as c:
            rv = c.get(url_for('recipes.categories', title=title))
            self.assertEqual(rv.status_code, 200)

    def test_api_get_recipe(self):
        title = 'json'
        recipe = self.create_recipe(title=title)
        rv = self.client.get('/api/v1/{0}'.format(recipe.id))
        data = json.loads(rv.data)
        self.assertEqual(data['title'], title)

    def test_api_get_recipes(self):
        title = 'recipes api'
        recipe = self.create_recipe(title=title)
        rv = self.client.get('/api/v1/recipes')
        data = json.loads(rv.data)
        self.assertEqual(data['has_next'], False)
        self.assertEqual(data['has_prev'], False)
        self.assertEqual(recipe.title, data['items'][0]['title'])
        self.assertEqual(data['page'], 1)
        self.assertEqual(data['pages'], 1)
        self.assertEqual(data['per_page'], 10)
        self.assertEqual(data['total'], 1)

if __name__ == '__main__':
    import unittest
    unittest.main()
