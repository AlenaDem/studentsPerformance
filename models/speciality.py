from db import open_db


class Speciality:
    def __init__(self, id, speciality_name=''):
        self.id = id
        self.speciality_name = speciality_name

    @staticmethod
    def get(id):
        db = open_db()
        try:
            db.cursor.execute('SELECT * FROM specialities WHERE id = %s', (id,))
            for record in db.cursor.fetchall():
                return Speciality(record['id'], record['speciality_name'])

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None

    @staticmethod
    def create(name):
        db = open_db()

        try:
            script = 'INSERT INTO specialities (speciality_name) VALUES (%s)'
            values = (name,)
            db.cursor.execute(script, values)
            db.conn.commit()
            return True

        except Exception as error:
            print(error)

        finally:
            db.close()

        return False

    @staticmethod
    def update(id, name):
        db = open_db()
        try:
            script = 'UPDATE specialities SET speciality_name=%s WHERE id=%s'
            values = (name, id)
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
            db.cursor.execute('SELECT * FROM specialities')

            items = []
            for record in db.cursor.fetchall():
                items.append(Speciality(record['id'], record['speciality_name']))
            return items

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None
