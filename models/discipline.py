from db import open_db


class Discipline:
    def __init__(self, id, discipline_name=''):
        self.id = id
        self.discipline_name = discipline_name

    @staticmethod
    def get(id):
        db = open_db()
        try:
            db.cursor.execute('SELECT * FROM disciplines WHERE id = %s', (id,))
            for record in db.cursor.fetchall():
                return Discipline(record['id'], record['discipline_name'])

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None

    @staticmethod
    def create(name):
        db = open_db()

        try:
            script = 'INSERT INTO disciplines (discipline_name) VALUES (%s)'
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
            script = 'UPDATE disciplines SET discipline_name=%s WHERE id=%s'
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
            db.cursor.execute('SELECT * FROM disciplines')

            items = []
            for record in db.cursor.fetchall():
                items.append(Discipline(record['id'], record['discipline_name']))
            return items

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None
