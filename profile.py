from flask import Blueprint, render_template, jsonify, request, session
from models.teacher import Teacher

profile = Blueprint('profile', __name__)


@profile.route('/disciplines_by_date', methods=['GET'])
def get_disciplines_by_date():
    args = request.args
    if 'year' not in args:
        return 500

    print(f"Запрос дисциплин от пользователя {session['user_id']}")
    teacher_id = session['user_id']
    year = args['year']
    semester = args['semester']

    disciplines = Teacher.get_disciplines(teacher_id, year, semester)
    data = dict()
    for k, name in disciplines:
        data[k] = name

    return jsonify(data)


@profile.route('/discipline-groups', methods=['GET'])
def get_groups_by_discipline():
    args = request.args

    print(f"request from user {session['user_id']}")
    teacher_id = session['user_id']
    discipline_id = args['discipline_id']
    academic_year = args['year']
    semester = args['semester']

    groups = Teacher.get_groups(discipline_id, academic_year, semester, teacher_id)

    data = dict()
    for k, name in groups:
        data[k] = name

    return jsonify(data)


@profile.route('/load_group_grades', methods=['GET'])
def load_group_grades():
    args = request.args

    print(f"request from user {session['user_id']}")
    teacher_id = session['user_id']
    discipline_id = args['discipline_id']
    group_id = args['group_id']
    academic_year = args['year']
    semester = args['semester']
    group_grades = Teacher.get_group_grades(academic_year, semester, discipline_id, group_id)

    data = dict()
    for *args, g, d in group_grades:
        full_name = ' '.join(args)
        if full_name not in data:
            data[full_name] = []
        data[full_name].append({'grade': g, 'date': d})

    return render_template('group_grades.html', group_grades=data)

@profile.route('/group-students', methods=['GET'])
def get_students_by_group():
    args = request.args

    print(f"request from user {session['user_id']}")
    group_id = args['group_id']

    students = Teacher.get_students(group_id)
    data = dict()
    for k, *args in students:
        data[k] = ' '.join(args)

    print(data)
    return jsonify(data)


@profile.route('/add_grade', methods=['POST'])
def add_grade():
    data = request.get_json(force=True)
    print(data)

    teacher_id = session['user_id']
    year = data['year']
    semester = data['semester']
    discipline_id = data['disciplineId']
    student_id = data['studentId']
    grade = data['grade']

    Teacher.set_grade(year, semester, teacher_id, discipline_id, student_id, grade)
    return jsonify(data)
