import os
import unittest
import tempfile
from app import app, db
from app.models import Recipe

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

    def create_recipe(self, **kwargs):
        new_recipe = Recipe(**kwargs)
        db.session.add(new_recipe)
        db.session.commit()
        return new_recipe

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries.' in rv.data

    def test_random_with_no_data(self):
        rv = self.app.get('/random')
        self.assertEqual(rv.status_code, 404)

    def test_random_with_data(self):
        recipe = self.create_recipe(title='random')
        rv = self.app.get('/random')
        self.assertEqual(rv.status_code, 200)
        assert recipe.title in rv.data

    def test_with_quantity(self):
        recipe = self.create_recipe(title='with quantity', quantity=1)
        rv = self.app.get('/{0}'.format(recipe.id))
        h1 = '{0} ({1})'.format(recipe.title, recipe.quantity)
        assert h1 in rv.data

    def test_without_quantity(self):
        recipe = self.create_recipe(title='without quantity', quantity=None)
        rv = self.app.get('/{0}'.format(recipe.id))
        h1 = '{0}'.format(recipe.title)
        assert h1 in rv.data

if __name__ == '__main__':
    unittest.main()
