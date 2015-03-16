import sys
from sqlalchemy import create_engine
from config import POSTGRES_HOST, POSTGRES_DB
from app import db

class DBManage(object):
    def __init__(self):
        self.host = POSTGRES_HOST
        self.engine = create_engine(self.host, echo=True)
        self.conn = self.engine.connect()

    def up(self, db_name=POSTGRES_DB):
        self.conn.execute("commit")
        self.conn.execute("create database {0}".format(db_name))
        self.conn.close()
        db.create_all()

    def down(self, db_name=POSTGRES_DB):
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
