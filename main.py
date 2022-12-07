from flask import Blueprint, render_template, session, redirect, url_for
from grade import Grade

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
def profile():
    print("profile")
    if "user_id" not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    grades = Grade.get_grades(user_id)
    return render_template('index.html', grades=grades)
