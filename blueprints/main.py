from flask import Blueprint, render_template, session, redirect, url_for
from models.grade import Grade
from models.user import Role
from validators import valid_session

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if not valid_session(session):
        return redirect(url_for('auth.login'))
    return render_template('index.html')


@main.route('/profile')
def profile():
    if not valid_session(session, log=False):
        return redirect(url_for('auth.login'))

    user_role = session['user_role']

    if user_role == Role.Student:
        return redirect(url_for('student_profile.profile'))

    if user_role == Role.Teacher:
        return redirect(url_for('teacher_profile.profile'))

    if user_role == Role.Admin:
        return redirect(url_for('manager_profile.profile'))

    return redirect(url_for('auth.login'))