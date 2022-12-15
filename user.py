import psycopg2
import psycopg2.extras

from db import open_db
from enum import IntEnum


class Role(IntEnum):
    Student = 1
    Teacher = 2
    Admin = 3


class User:
    def __init__(self, id, login, password, role):
        self.id = id
        self.login = login
        self.password = password
        self.role = role

    @staticmethod
    def get_user(login):
        db = open_db()
        try:
            db.cursor.execute('SELECT * FROM users WHERE login = %s', (login,))
            for record in db.cursor.fetchall():
                return User(record['id'], record['login'], record['password'], record['role'])

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None
