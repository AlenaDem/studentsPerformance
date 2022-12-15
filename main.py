from flask import Blueprint, render_template, session, redirect, url_for
from grade import Grade
from user import Role
from validators import valid_session

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
def profile():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_role = session['user_role']

    if user_role != Role.Student:
        return redirect(url_for('main.index'))

    print('Student opens profile:', user_id)

    grades = Grade.get_grades(user_id)

    grade_map = dict()
    for grade in grades:
        year = grade['academic_year']
        if year not in grade_map:
            grade_map[year] = dict()
        semester = grade['semester']
        if semester not in grade_map[year]:
            grade_map[year][semester] = []
        grade_map[year][semester].append(grade)

    for y in sorted(grade_map.keys()):
        for s in sorted(grade_map[y].keys()):
            print(y, s, grade_map[y][s])

    return render_template('student_profile.html', grades=grade_map)


@main.route('/teacher_profile', methods=['GET'])
def teacher_profile():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_role = session['user_role']

    if user_role != Role.Teacher:
        return redirect(url_for('main.index'))

    print('Teacher opens profile:', user_id)

    return render_template('teacher_profile.html')

@main.route('/admin_profile', methods=['GET'])
def admin_profile():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_role = session['user_role']

    if user_role != Role.Admin:
        return redirect(url_for('main.index'))

    print('Admin opens profile:', user_id)

    return render_template('admin_profile.html')
