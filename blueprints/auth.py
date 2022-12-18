from flask import Blueprint, render_template, redirect, url_for, request, flash, session

from app import app
from helpers import hash_password, log_request_info
from models.user import User, Role
from validators import valid_session

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    log_request_info(request)

    if valid_session(session, log=False):
        return redirect(url_for('main.index'))

    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    log_request_info(request)

    login = request.form.get('login')
    password = request.form.get('password')
    password = hash_password(password)

    user = User.get_by_login(login)

    if user is None or user.password != password:
        flash('Логин или пароль неверны, попробуйте снова.')
        app.logger.info(f"Неуспешная попытка входа с логином '{login}'")
        return redirect(url_for('auth.login'))

    session["user_id"] = user.id
    session["user_role"] = user.role
    session["username"] = user.login

    app.logger.info(f"Пользователь '{user.login}' успешно вошел в систему")

    return redirect(url_for('main.profile'))


@auth.route('/logout', methods=['GET'])
def logout():
    log_request_info(request)

    if not valid_session(session):
        return redirect(url_for('auth.login'))

    app.logger.info(f"Пользователь '{session['username']}' вышел из системы")

    session.pop("user_id")
    session.pop("user_role")
    session.pop("username")
    return redirect(url_for('auth.login'))
