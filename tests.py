import os
import unittest
import tempfile
from app import app, db

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

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries.' in rv.data

if __name__ == '__main__':
    unittest.main()
