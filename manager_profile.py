from flask import Blueprint, render_template, request, session, url_for, redirect

from helpers import hash_password
from models.group import Group
from models.student import Student
from models.user import Role, User
from validators import valid_session, valid_args

manager_profile = Blueprint('manager_profile', __name__)


@manager_profile.route('/student_list', methods=['GET'])
def student_list():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_role = session['user_role']
    if user_role != Role.Admin:
        return redirect(url_for('main.index'))

    students = Student.get_all()
    data = []
    for student in students:
        full_name = ' '.join((student.last_name, student.first_name, student.patronymic))
        group = Group.get(student.group_id)
        group_name = "-" if group is None else group.group_name
        data.append({'id': student.id,
                     'name': full_name,
                     'group_id': student.group_id,
                     'group': group_name,
                     'date': student.admission_date})

    return render_template('student_list.html', data=data)


@manager_profile.route('/edit_student_form/<student_id>', methods=['GET'])
def edit_student_form(student_id):
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    student = Student.get(student_id)
    if student is None:
        return '', 404

    user = User.get(student_id)
    if user is None:
        return '', 404

    groups = Group.get_all()
    if groups is None or len(groups) == 0:
        return '', 404

    return render_template('student_edit.html', student=student, user=user, groups=groups)


@manager_profile.route('/create_student_form', methods=['GET'])
def create_student_form():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    groups = Group.get_all()
    if groups is None or len(groups) == 0:
        return '', 404

    empty_student = Student(0)
    empty_student.group_id = groups[0].id

    empty_user = User(0)

    return render_template('student_edit.html', student=empty_student, user=empty_user, groups=groups)


@manager_profile.route('/create_student', methods=['POST'])
def create_student():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    data = request.get_json(force=True)
    if not valid_args(data, 'first_name', 'last_name', 'group_id', 'login', 'password', 'patronymic', 'year'):
        return '', 500

    ok = Student.create(login=data["login"],
                        password=hash_password(data['password']),
                        first_name=data['first_name'],
                        last_name=data['last_name'],
                        patronymic=data['patronymic'],
                        admission_date=data['year'],
                        group_id=data['group_id'])

    if not ok:
        return '', 500

    return '', 200


@manager_profile.route('/edit_student', methods=['POST'])
def edit_student():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    data = request.get_json(force=True)
    if not valid_args(data, 'id', 'first_name', 'last_name', 'group_id', 'patronymic', 'year'):
        return '', 500

    if not Student.update(id=data['id'],
                          first_name=data['first_name'],
                          last_name=data['last_name'],
                          patronymic=data['patronymic'],
                          group_id=data['group_id'],
                          admission_date=data['year']):
        return '', 500

    return '', 200


@manager_profile.route('/delete_student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    print(f'Delete student {student_id}')

    if not Student.delete(student_id):
        return '', 500

    return '', 200
