from db import open_db


class GroupDiscipline:
    def __init__(self, id, academic_year=2022, semester=1, discipline_id=None, teacher_id=None, group_id=None):
        self.id = id
        self.academic_year = academic_year
        self.semester = semester
        self.discipline_id = discipline_id
        self.teacher_id = teacher_id
        self.group_id = group_id

    @staticmethod
    def get(id):
        db = open_db()
        try:
            db.cursor.execute('SELECT * FROM group_disciplines WHERE id = %s', (id,))
            for record in db.cursor.fetchall():
                return GroupDiscipline(id=record['id'],
                                       academic_year=record['academic_year'],
                                       semester=record['semester'],
                                       discipline_id=record['discipline_id'],
                                       teacher_id=record['teacher_id'],
                                       group_id=record['group_id']
                                       )

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None

    @staticmethod
    def create(academic_year, semester, discipline_id, teacher_id, group_id):
        db = open_db()

        try:
            script = 'INSERT INTO group_disciplines (academic_year, semester, discipline_id, teacher_id, group_id) ' \
                     'VALUES (%s, %s, %s, %s, %s)'
            values = (academic_year, semester, discipline_id, teacher_id, group_id)
            db.cursor.execute(script, values)
            db.conn.commit()
            return True

        except Exception as error:
            print(error)

        finally:
            db.close()

        return False

    @staticmethod
    def update(id, academic_year, semester, discipline_id, teacher_id, group_id):
        db = open_db()
        try:
            script = 'UPDATE group_disciplines SET ' \
                     'academic_year=%s, ' \
                     'semester=%s, ' \
                     'discipline_id=%s, ' \
                     'teacher_id=%s, ' \
                     'group_id=%s ' \
                     'WHERE id=%s'
            values = (academic_year, semester, discipline_id, teacher_id, group_id, id)
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
            db.cursor.execute('SELECT * FROM group_disciplines ')

            items = []
            for record in db.cursor.fetchall():
                items.append(GroupDiscipline(id=record['id'],
                                             academic_year=record['academic_year'],
                                             semester=record['semester'],
                                             discipline_id=record['discipline_id'],
                                             teacher_id=record['teacher_id'],
                                             group_id=record['group_id']
                                             ))
            return items

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None

    @staticmethod
    def get_by_group_id(id):
        db = open_db()
        try:
            script = 'SELECT * FROM group_disciplines WHERE group_id = %s'
            values = (id,)
            db.cursor.execute(script, values)

            items = []
            for record in db.cursor.fetchall():
                items.append(GroupDiscipline(id=record['id'],
                                             academic_year=record['academic_year'],
                                             semester=record['semester'],
                                             discipline_id=record['discipline_id'],
                                             teacher_id=record['teacher_id'],
                                             group_id=record['group_id']
                                             ))
            return items

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None


    @staticmethod
    def delete(id):
        db = open_db()
        try:
            script = 'DELETE FROM group_disciplines WHERE id=%s'
            db.cursor.execute(script, (id,))
            db.conn.commit()
            return True

        except Exception as error:
            print(error)

        finally:
            db.close()

        return False

