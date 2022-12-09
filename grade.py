import psycopg2
import psycopg2.extras

from db import open_db


class Grade:
    def __init__(self, id, student_id, teacher_id, discipline_id, grade, datetime, semester):
        self.id = id
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.discipline_id = discipline_id
        self.grade = grade
        self.datetime = datetime
        self.semester = semester

    @staticmethod
    def get_grades(student_id):
        db = open_db()
        try:
            db.cursor.execute('SELECT disciplines.discipline_name, grades.grade, grades.datetime, grades.semester '
                              'FROM grades '
                              'JOIN disciplines ON grades.discipline_id = disciplines.id '
                              'WHERE grades.student_id = %s', (student_id,))

            grades_list = db.cursor.fetchall()
            return grades_list

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None
