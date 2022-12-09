from flask import Blueprint, render_template, session, redirect, url_for
from grade import Grade

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('login.html')


@main.route('/profile')
def profile():
    if "user_id" not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    grades = Grade.get_grades(user_id)

    grade_map = dict()
    for grade in grades:
        year = grade['datetime'].year
        if year not in grade_map:
            grade_map[year] = dict()
        semester = grade['semester']
        if semester not in grade_map[year]:
            grade_map[year][semester] = []
        grade_map[year][semester].append(grade)

    for y in sorted(grade_map.keys()):
        for s in sorted(grade_map[y].keys()):
            print(y, s, grade_map[y][s])

    return render_template('index.html', grades=grade_map)

@main.route('/teacher_profile')
def teacher_profile():
    if "user_id" not in session:
        return redirect(url_for('auth.login'))

    return render_template('teacher_profile.html')
