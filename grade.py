import psycopg2
import psycopg2.extras

from db import open_db


class Grade:
    def __init__(self, id, student_id, teacher_id, discipline_id, grade, datetime, timepoint_id):
        self.id = id
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.discipline_id = discipline_id
        self.grade = grade
        self.datetime = datetime
        self.timepoint_id = timepoint_id

    @staticmethod
    def get_grades(student_id):
        db = open_db()
        try:
            db.cursor.execute('SELECT * FROM grades WHERE student_id = %s', (student_id,))
            grade_list = []
            for record in db.cursor.fetchall():
                grade_list.append(Grade(record['id'], record['teacher_id'],
                                        record['discipline_id'], record['grade'],
                                        record['datetime'], record['timepoint_id']))
            return grade_list;

        except Exception as error:
            print(error)

        finally:
            db.close()

        return None
