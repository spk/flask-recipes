import os
import unittest
import tempfile
from contextlib import contextmanager
from app import app, db
from app.models import Recipe, Category
from flask import url_for

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_name = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_name
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_name)

    @contextmanager
    def create_recipe(self, **kwargs):
        new_recipe = Recipe(**kwargs)
        db.session.add(new_recipe)
        db.session.commit()
        yield new_recipe

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries.' in rv.data

    def test_random_with_no_data(self):
        rv = self.app.get('/random')
        self.assertEqual(rv.status_code, 404)

    def test_random_with_data(self):
        with self.create_recipe(title='random') as recipe:
            rv = self.app.get('/random')
            self.assertEqual(rv.status_code, 200)
            assert recipe.title in rv.data

    def test_with_quantity(self):
        with self.create_recipe(title='with quantity', quantity=1) as recipe:
            rv = self.app.get('/{0}'.format(recipe.id))
            h1 = '{0} ({1})'.format(recipe.title, recipe.quantity)
            assert h1 in rv.data

    def test_without_quantity(self):
        with self.create_recipe(title='without quantity', quantity=None) as recipe:
            rv = self.app.get('/{0}'.format(recipe.id))
            h1 = '{0}'.format(recipe.title)
            assert h1 in rv.data

    def test_without_categories(self):
        with app.test_request_context():
            rv = self.app.get(url_for('categories', title='None'))
            self.assertEqual(rv.status_code, 404)

    def test_with_categories(self):
        title = 'category'
        categories = [Category(title=title)]
        with self.create_recipe(title='title', quantity=10, categories=categories) as recipe:
            with app.test_request_context():
                rv = self.app.get(url_for('categories', title=title))
                self.assertEqual(rv.status_code, 200)

    def test_xml_format(self):
        categories = [Category(title='category title')]
        with self.create_recipe(title='title', quantity=10, categories=categories) as recipe:
            rv = self.app.get('/{0}.xml'.format(recipe.id))
            title = "<title>{0}</title>".format(recipe.title)
            quantity = "<yield>{0}</yield>".format(recipe.quantity)
            cat = "<cat>{0}</cat>".format(recipe.categories[0].title)
            assert title in rv.data
            assert quantity in rv.data
            assert cat in rv.data

if __name__ == '__main__':
    unittest.main()
