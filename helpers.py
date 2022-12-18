import hashlib
from app import app


def log_request_info(request):
    app.logger.info(f'{request.method} {request.path}/{request.query_string.decode()}')

    if request.method == "POST":
        try:
            data = request.get_json(force=True)
            app.logger.info(f"Request data: {data}")
        except Exception as e:
            return

def hash_password(password):
    salt = "8gwe"
    password = password + salt
    password = hashlib.sha256(password.encode()).hexdigest()
    return password
