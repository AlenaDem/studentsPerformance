from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for

from app import app
from helpers import log_request_info
from models.teacher import Teacher
from models.user import Role
from validators import valid_session, valid_args

teacher_profile = Blueprint('teacher_profile', __name__)


@teacher_profile.route('/teacher_profile', methods=['GET'])
def profile():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_role = session['user_role']
    username = session['username']

    if user_role != Role.Teacher:
        return redirect(url_for('main.index'))

    app.logger.info(f"Пользователь {user_id}:{username} зашел в профиль учителя")

    return render_template('teacher_profile.html')


@teacher_profile.route('/disciplines_by_date', methods=['GET'])
def get_disciplines_by_date():
    log_request_info(request)

    if not valid_session(session):
        return redirect(url_for('auth.login'))

    args = request.args
    user_id = session['user_id']
    user_role = session['user_role']
    username = session['username']
    if user_role != Role.Teacher:
        return redirect(url_for('main.index'))

    if not valid_args(args, 'year', 'semester'):
        return 'Некорректные данные', 500

    teacher_id = user_id
    year = args['year']
    semester = args['semester']

    disciplines = Teacher.get_disciplines(teacher_id, year, semester)
    data = dict()
    for k, name in disciplines:
        data[k] = name

    app.logger.info(f"Пользователь {user_id}:{username} запросил список дисциплин")

    return jsonify(data)


@teacher_profile.route('/discipline-groups', methods=['GET'])
def get_groups_by_discipline():
    log_request_info(request)

    if not valid_session(session):
        return redirect(url_for('auth.login'))

    args = request.args
    user_id = session['user_id']
    user_role = session['user_role']
    username = session['username']
    if user_role != Role.Teacher:
        return redirect(url_for('main.index'))

    if not valid_args(args, 'year', 'semester', 'discipline_id'):
        return 'Некорректные данные', 500

    teacher_id = user_id
    discipline_id = args['discipline_id']
    academic_year = args['year']
    semester = args['semester']

    groups = Teacher.get_groups(discipline_id, academic_year, semester, teacher_id)

    data = dict()
    for k, name in groups:
        data[k] = name

    app.logger.info(f"Пользователь {user_id}:{username} запрос список групп по дисциплине")

    return jsonify(data)


@teacher_profile.route('/load_group_grades', methods=['GET'])
def load_group_grades():
    log_request_info(request)

    if not valid_session(session):
        return redirect(url_for('auth.login'))

    args = request.args
    user_id = session['user_id']
    user_role = session['user_role']
    username = session['username']
    if user_role != Role.Teacher:
        return redirect(url_for('main.index'))

    if not valid_args(args, 'year', 'semester', 'discipline_id', 'group_id'):
        return 'Некорректные данные', 500

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

    app.logger.info(f"Пользователь {user_id}:{username} запросил оценки группы по дисциплине")
    return render_template('group_grades.html', group_grades=data)


@teacher_profile.route('/group-students', methods=['GET'])
def get_students_by_group():
    log_request_info(request)

    if not valid_session(session):
        return redirect(url_for('auth.login'))

    args = request.args
    user_id = session['user_id']
    user_role = session['user_role']
    username = session['username']
    if user_role != Role.Teacher:
        return redirect(url_for('main.index'))

    if not valid_args(args, 'group_id'):
        return 'Некорректные данные', 500

    group_id = args['group_id']

    students = Teacher.get_students(group_id)
    data = dict()
    for k, *args in students:
        data[k] = ' '.join(args)

    app.logger.info(f"Пользователь {user_id}:{username} запросил список студентов")

    return jsonify(data)


@teacher_profile.route('/add_grade', methods=['POST'])
def add_grade():
    log_request_info(request)

    if not valid_session(session):
        return redirect(url_for('auth.login'))

    data = request.get_json(force=True)
    user_id = session['user_id']
    user_role = session['user_role']
    username = session['username']
    if user_role != Role.Teacher:
        return redirect(url_for('main.index'))

    if not valid_args(data, 'year', 'semester', 'disciplineId', 'studentId', 'grade'):
        app.logger.error(f"Некорректные аргументы запроса")
        return 'Некорректные данные', 500

    teacher_id = session['user_id']
    year = data['year']
    semester = data['semester']
    discipline_id = data['disciplineId']
    student_id = data['studentId']
    grade = data['grade']

    Teacher.set_grade(year, semester, teacher_id, discipline_id, student_id, grade)

    app.logger.info(f"Пользователь {user_id}:{username} поставил оценку")

    return jsonify(data)
