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

