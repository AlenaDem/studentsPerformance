from db import open_db


class Student:
    def __init__(self, id, first_name, last_name, patronymic, admission_date, group_id):
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
    def update(student):
        db = open_db()
        try:
            db.cursor.execute(f"UPDATE students SET first_name='{student.first_name}', "
                              f"last_name='{student.last_name}', "
                              f"patronymic='{student.patronymic}', "
                              f"group_id={student.group_id} "
                              f"WHERE id={student.id}"
                              )
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
            db.cursor.execute('SELECT * FROM students ')

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
