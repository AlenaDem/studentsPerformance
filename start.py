from flask import Flask, session
from auth import auth as auth_blueprint
from main import main as main_blueprint
from profile import profile as profile_blueprint
from manager_profile import manager_profile


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(manager_profile)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
