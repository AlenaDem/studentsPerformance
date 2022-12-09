from flask import Blueprint, render_template, redirect, url_for, request, flash, session
import hashlib
from user import User

auth = Blueprint('auth', __name__)
salt = "8gwe"


@auth.route('/login')
def login():
    return render_template('login.html')

def hash_password(password):
    password = password + salt
    password = hashlib.sha256(password.encode()).hexdigest()
    return password


@auth.route('/login', methods=['POST'])
def login_post():
    login = request.form.get('login')
    password = request.form.get('password')
    password = hash_password(password)
    print(password)

    user = User.get_user(login)

    if user is None or user.password != password:
        flash('Логин или пароль неверны, попробуйте снова.')
        return redirect(url_for('auth.login'))

    session["user_id"] = user.id

    if user.role == 1:
        return redirect(url_for('main.profile'))

    if user.role == 2:
        return redirect(url_for('main.teacher_profile'))
