from app import app


def valid_session(session, log=True):
    if "user_id" not in session or "user_role" not in session or "username" not in session or "2fa" not in session:
        if log:
            app.logger.error("Сессия невалидна!")
        return False

    if not session["2fa"]:
        if log:
            app.logger.error("Сессия невалидна!")
        return False

    return True


def valid_session_without2fa(session, log=True):
    if "user_id" not in session or "user_role" not in session or "username" not in session:
        if log:
            app.logger.error("Сессия невалидна!")
        return False

    return True


def valid_args(data, *args):
    for arg_name in args:
        if arg_name not in data:
            return False
    return True
