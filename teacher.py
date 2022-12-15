from db import open_db


class Teacher:
    def __init__(self, id, first_name, last_name, patronymic):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.patronymic = patronymic

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
