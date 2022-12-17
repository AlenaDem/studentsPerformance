from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from helpers import hash_password
from models.user import User, Role
from validators import valid_session

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if valid_session(session):
        return redirect(url_for('main.index'))

    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    login = request.form.get('login')
    password = request.form.get('password')
    password = hash_password(password)
    print(password)

    user = User.get_by_login(login)

    if user is None or user.password != password:
        flash('Логин или пароль неверны, попробуйте снова.')
        return redirect(url_for('auth.login'))

    session["user_id"] = user.id
    session["user_role"] = user.role

    if user.role == Role.Student:
        return redirect(url_for('main.student_profile'))

    if user.role == Role.Teacher:
        return redirect(url_for('main.teacher_profile'))

    if user.role == Role.Admin:
        return redirect(url_for('main.manager_profile'))

    return redirect(url_for('main.index'))


@auth.route('/logout', methods=['GET'])
def logout():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    session.pop("user_id")
    session.pop("user_role")
    return redirect(url_for('auth.login'))