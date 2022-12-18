from flask import Blueprint, render_template, session, url_for, redirect

from app import app
from models.grade import Grade
from models.user import Role
from validators import valid_session

student_profile = Blueprint('student_profile', __name__)


@student_profile.route('/student_profile')
def profile():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_role = session['user_role']
    username = session['username']

    if user_role != Role.Student:
        return redirect(url_for('main.index'))

    app.logger.info(f"Пользователь {user_id}:{username} зашел в профиль студента")

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


