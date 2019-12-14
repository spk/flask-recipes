import sys
from sqlalchemy import create_engine
from app import create_app
import app.models
from app.extensions import db
from app.config import config, SELECTED_CONFIG

class DBManage(object):
    def __init__(self):
        self.host = config[SELECTED_CONFIG].POSTGRES_HOST
        self.engine = create_engine(self.host, echo=True)
        self.conn = self.engine.connect()

    def up(self, db_name=config[SELECTED_CONFIG].POSTGRES_DB):
        self.conn.execute("commit")
        self.conn.execute("create database {0}".format(db_name))
        self.conn.close()
        app = create_app()
        with app.app_context():
            db.create_all()

    def down(self, db_name=config[SELECTED_CONFIG].POSTGRES_DB):
        self.conn.execute("commit")
        self.conn.execute("drop database {0}".format(db_name))
        self.conn.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('USAGE: {0} [up|down]'.format(sys.argv[0]))
        sys.exit(1)
    else:
        if sys.argv[1] == "up":
            DBManage().up()
            sys.exit(0)
        elif sys.argv[1] == "down":
            DBManage().down()
            sys.exit(0)
