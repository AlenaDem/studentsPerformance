import psycopg2
import psycopg2.extras
from config import hostname, database, username, pwd, port_id

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open(self):
        try:
            self.conn = psycopg2.connect(host=hostname, dbname=database, user=username, password=pwd, port=port_id)
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            return True

        except Exception as error:
            self.close()
            return False

    def close(self):
        if self.cursor is not None:
            self.cursor.close()

        if self.conn is not None:
            self.conn.close()


def open_db():
    db = Database()
    if db.open():
        return db

    return None

