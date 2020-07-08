import sys
from sqlalchemy import create_engine, inspect
from app import create_app
from app.extensions import db
from app.config import config, SELECTED_CONFIG


class DBManage(object):
    def __init__(self):
        self.url = config[SELECTED_CONFIG].POSTGRES_URL
        self.engine = create_engine(self.url, echo=True)

    def up(self, db_name=config[SELECTED_CONFIG].POSTGRES_DB):
        connection = self.engine.connect()
        connection.execute("COMMIT")
        connection.execute("CREATE DATABASE {0}".format(db_name))
        connection.close()
        self.create()

    def down(self, db_name=config[SELECTED_CONFIG].POSTGRES_DB):
        connection = self.engine.connect()
        connection.execute("COMMIT")
        connection.execute("DROP DATABASE {0}".format(db_name))
        connection.close()

    def create(self):
        app = create_app()
        with app.app_context():
            db.create_all()

    def drop(self):
        engine = create_engine(
            config[SELECTED_CONFIG].SQLALCHEMY_DATABASE_URI,
            echo=True)
        connection = engine.connect()
        inspector = inspect(engine)
        for table_name in inspector.get_table_names():
            connection.execute("DROP TABLE {0} CASCADE".format(table_name))
        connection.close()


if __name__ == '__main__':
    options = {
        "up": DBManage().up,
        "down": DBManage().down,
        "create": DBManage().create,
        "drop": DBManage().drop
    }
    if sys.argv[1] in options:
        options[sys.argv[1]]()
        sys.exit(0)
    else:
        print('USAGE: {0} [{1}]'.format(sys.argv[0], "|".join(options.keys())))
        sys.exit(1)
