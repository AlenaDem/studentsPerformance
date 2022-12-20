from db import open_db


class Otp:
    def __init__(self, id, secret):
        self.id = id
        self.secret = secret

    @staticmethod
    def get(id):
        db = open_db()
        try:
            db.cursor.execute('SELECT * FROM otp WHERE id = %s', (id,))
            for record in db.cursor.fetchall():
                return Otp(record['id'], record['secret'])

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None

    @staticmethod
    def create(id, secret):
        db = open_db()

        try:
            script = 'INSERT INTO otp (id, secret) VALUES (%s, %s)'
            values = (id, secret)
            db.cursor.execute(script, values)
            db.conn.commit()
            return True

        except Exception as error:
            print(error)

        finally:
            db.close()

        return False
