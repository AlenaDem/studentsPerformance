from io import BytesIO

import pyotp
import pyqrcode
from flask import Blueprint, render_template, redirect, url_for, request, flash, session

from app import app
from helpers import hash_password, log_request_info
from models.otp import Otp
from models.user import User, Role
from validators import valid_session, valid_session_without2fa

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
    session["2fa"] = False

    # app.logger.info(f"Пользователь '{user.login}' успешно вошел в систему")
    # return redirect(url_for('main.profile'))

    return redirect(url_for('auth.login_2fa'))


@auth.route("/login_2fa")
def login_2fa():
    if not valid_session_without2fa(session, log=False):
        return redirect(url_for('auth.login'))

    if session["2fa"]:
        return redirect(url_for("main.profile"))

    otpdata = Otp.get(session["user_id"])
    need_register = otpdata is None

    return render_template("login2fa.html", need_register=need_register)


@auth.route('/qrcode2fa')
def qrcode2fa():
    if not valid_session_without2fa(session, log=False):
        return '', 404

    secret = pyotp.random_base32()
    session["2fa_secret"] = secret
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=session["username"], issuer_name='student_perf')
    url = pyqrcode.create(uri)
    stream = BytesIO()
    url.svg(stream, scale=5)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@app.route("/login_2fa", methods=["POST"])
def login_2fa_form():
    if not valid_session_without2fa(session, log=False):
        return '', 404

    otpdata = Otp.get(session["user_id"])
    if otpdata is not None:
        session["2fa_secret"] = otpdata.secret
    secret = session["2fa_secret"]

    otp = request.form.get("otp")
    if pyotp.TOTP(secret).verify(otp):
        if otpdata is None:
            if not Otp.create(session["user_id"], secret):
                return redirect(url_for("auth.login"))

        session["2fa"] = True
        session.pop("2fa_secret")
        flash("Успешно", "success")
        return redirect(url_for("main.profile"))
    else:
        session.pop("2fa_secret")
        session.pop("2fa")
        flash("Неправильный одноразовый пароль", "danger")
        return redirect(url_for("auth.login"))


@auth.route('/logout', methods=['GET'])
def logout():
    log_request_info(request)

    if not valid_session(session):
        return redirect(url_for('auth.login'))

    app.logger.info(f"Пользователь '{session['username']}' вышел из системы")

    session.pop("user_id")
    session.pop("user_role")
    session.pop("username")
    session.pop("2fa")
    return redirect(url_for('auth.login'))
