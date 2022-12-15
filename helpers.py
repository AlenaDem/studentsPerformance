import hashlib


def hash_password(password):
    salt = "8gwe"
    password = password + salt
    password = hashlib.sha256(password.encode()).hexdigest()
    return password
