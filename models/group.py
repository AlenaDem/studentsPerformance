from db import open_db


class Group:
    def __init__(self, id, speciality_id, course, group_name):
        self.id = id
        self.speciality_id = speciality_id
        self.course = course
        self.group_name = group_name

    @staticmethod
    def get(id):
        db = open_db()
        try:
            db.cursor.execute('SELECT * FROM st_groups WHERE id = %s', (id,))
            for record in db.cursor.fetchall():
                return Group(record['id'],
                             record['speciality_id'],
                             record['course'],
                             record['group_name']
                             )

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None

    @staticmethod
    def get_all():
        db = open_db()
        try:
            db.cursor.execute('SELECT * FROM st_groups ')

            items = []
            for record in db.cursor.fetchall():
                items.append(Group(record['id'],
                                   record['speciality_id'],
                                   record['course'],
                                   record['group_name']
                                   ))
            return items

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None
