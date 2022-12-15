
def valid_session(session):
    if "user_id" not in session or "user_role" not in session:
        return False
    return True

