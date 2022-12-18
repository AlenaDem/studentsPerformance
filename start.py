from blueprints.auth import auth as auth_blueprint
from blueprints.main import main as main_blueprint
from blueprints.teacher_profile import teacher_profile
from blueprints.manager_profile import manager_profile
from blueprints.student_profile import student_profile
from app import app, init_logger

if __name__ == "__main__":
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(teacher_profile)
    app.register_blueprint(manager_profile)
    app.register_blueprint(student_profile)

    init_logger()
    app.run(debug=True)
