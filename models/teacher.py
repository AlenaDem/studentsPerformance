from db import open_db
from models.user import Role


class Teacher:
    def __init__(self, id, first_name='', last_name='', patronymic=''):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.patronymic = patronymic

    @staticmethod
    def get(id):
        db = open_db()
        try:
            db.cursor.execute('SELECT * FROM teachers WHERE id = %s', (id,))
            for record in db.cursor.fetchall():
                return Teacher(record['id'],
                               record['first_name'],
                               record['last_name'],
                               record['patronymic']
                               )

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None

    @staticmethod
    def create(login, password, first_name, last_name, patronymic):
        db = open_db()

        try:
            script = 'INSERT INTO users (login, password, role) VALUES (%s, %s, %s) RETURNING id'
            values = (login, password, Role.Teacher)
            db.cursor.execute(script, values)
            user_id = db.cursor.fetchone()[0]

            script = 'INSERT INTO teachers (id, last_name, first_name, patronymic) ' \
                     'VALUES (%s, %s, %s, %s)'
            values = (user_id, last_name, first_name, patronymic)
            db.cursor.execute(script, values)

            db.conn.commit()
            return True

        except Exception as error:
            print(error)

        finally:
            db.close()

        return False

    @staticmethod
    def update(id, first_name, last_name, patronymic):
        db = open_db()
        try:
            script = 'UPDATE teachers SET first_name=%s, last_name=%s, patronymic=%s ' \
                     'WHERE id=%s'
            values = (first_name, last_name, patronymic, id)
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
            db.cursor.execute('SELECT * FROM teachers')

            items = []
            for record in db.cursor.fetchall():
                items.append(Teacher(record['id'],
                                        record['first_name'],
                                        record['last_name'],
                                        record['patronymic']
                                        ))
            return items

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None

    @staticmethod
    def get_disciplines(teacher_id, academic_year, semester):
        db = open_db()
        try:
            db.cursor.execute('SELECT DISTINCT group_disciplines.discipline_id, disciplines.discipline_name '
                              'FROM group_disciplines '
                              'JOIN disciplines ON group_disciplines.discipline_id = disciplines.id '
                              'WHERE group_disciplines.academic_year = %s '
                              'AND group_disciplines.semester = %s '
                              'AND group_disciplines.teacher_id = %s', (academic_year, semester, teacher_id,))

            disciplines_list = db.cursor.fetchall()
            return disciplines_list

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None

    @staticmethod
    def get_groups(discipline_id, academic_year, semester, teacher_id):
        db = open_db()
        try:
            db.cursor.execute('SELECT DISTINCT group_disciplines.group_id, st_groups.group_name '
                              'FROM group_disciplines '
                              'JOIN st_groups ON group_disciplines.group_id = st_groups.id '
                              'WHERE group_disciplines.discipline_id = %s '
                              'AND group_disciplines.academic_year = %s '
                              'AND group_disciplines.semester = %s '
                              'AND group_disciplines.teacher_id = %s',
                              (discipline_id, academic_year, semester, teacher_id,))

            groups_list = db.cursor.fetchall()
            return groups_list

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None

    @staticmethod
    def get_students(group_id):
        db = open_db()
        try:
            db.cursor.execute('SELECT id, last_name, first_name, patronymic FROM students WHERE group_id = %s',
                              (group_id,))

            students_list = db.cursor.fetchall()
            return students_list

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None

    @staticmethod
    def set_grade(year, semester, teacher_id, discipline_id, student_id, grade):
        db = open_db()
        try:
            insert_script = 'INSERT INTO grades ' \
                            '(student_id, teacher_id, discipline_id, grade, academic_year, semester) ' \
                            'VALUES (%s, %s, %s, %s, %s, %s)'
            db.cursor.execute(insert_script, (student_id, teacher_id, discipline_id, grade, year, semester))
            db.conn.commit()

            print("Оценка поставлена")

            return None

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None

    @staticmethod
    def get_group_grades(academic_year, semester, discipline_id, group_id):
        db = open_db()
        try:
            db.cursor.execute('SELECT students.last_name, students.first_name, students.patronymic, '
                              'grades.grade, grades.datetime '
                              'FROM grades JOIN students ON students.id = grades.student_id '
                              'WHERE grades.academic_year = %s AND grades.semester = %s '
                              'AND grades.discipline_id = %s AND students.group_id = %s',
                              (academic_year, semester, discipline_id, group_id,))

            students_list = db.cursor.fetchall()
            return students_list

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None
