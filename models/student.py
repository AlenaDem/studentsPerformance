from db import open_db
from models.user import Role


class Student:
    def __init__(self, id, first_name='', last_name='', patronymic='', admission_date=2022, group_id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.patronymic = patronymic
        self.admission_date = admission_date
        self.group_id = group_id


    @staticmethod
    def get(id):
        db = open_db()
        try:
            db.cursor.execute('SELECT * FROM students WHERE id = %s', (id,))
            for record in db.cursor.fetchall():
                return Student(record['id'],
                               record['first_name'],
                               record['last_name'],
                               record['patronymic'],
                               record['admission_date'],
                               record['group_id'])

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None

    @staticmethod
    def create(login, password, first_name, last_name, patronymic, admission_date, group_id):
        db = open_db()

        try:
            script = 'INSERT INTO users (login, password, role) VALUES (%s, %s, %s) RETURNING id'
            values = (login, password, Role.Student)
            db.cursor.execute(script, values)
            user_id = db.cursor.fetchone()[0]

            script = 'INSERT INTO students (id, last_name, first_name, patronymic, group_id, admission_date) ' \
                     'VALUES (%s, %s, %s, %s, %s, %s)'
            values = (user_id, last_name, first_name, patronymic, group_id, admission_date)
            db.cursor.execute(script, values)

            db.conn.commit()
            return True

        except Exception as error:
            print(error)

        finally:
            db.close()

        return False

    @staticmethod
    def update(id, first_name, last_name, patronymic, group_id, admission_date):
        db = open_db()
        try:
            script = 'UPDATE students SET first_name=%s, last_name=%s, patronymic=%s, group_id=%s, admission_date=%s ' \
                     'WHERE id=%s'
            values = (first_name, last_name, patronymic, group_id, admission_date, id)
            db.cursor.execute(script, values)
            db.conn.commit()
            return True

        except Exception as error:
            print(error)

        finally:
            db.close()

        return False

    @staticmethod
    def get_all():
        db = open_db()
        try:
            db.cursor.execute('SELECT * FROM students')

            students = []
            for record in db.cursor.fetchall():
                students.append(Student(record['id'],
                                        record['first_name'],
                                        record['last_name'],
                                        record['patronymic'],
                                        record['admission_date'],
                                        record['group_id']))
            return students

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None

    @staticmethod
    def delete(id):
        db = open_db()
        try:
            script = 'DELETE FROM students WHERE id=%s'
            db.cursor.execute(script, (id,))

            script = 'DELETE FROM users WHERE id=%s'
            db.cursor.execute(script, (id,))

            db.conn.commit()
            return True

        except Exception as error:
            print(error)

        finally:
            db.close()

        return False
