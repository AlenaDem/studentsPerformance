
def valid_session(session):
    if "user_id" not in session or "user_role" not in session:
        return False
    return True


def valid_args(data, *args):
    for arg_name in args:
        if arg_name not in data:
            return False
    return True
