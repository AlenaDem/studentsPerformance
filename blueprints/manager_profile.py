from flask import Blueprint, render_template, request, session, url_for, redirect

from helpers import hash_password
from models.discipline import Discipline
from models.group import Group
from models.speciality import Speciality
from models.student import Student
from models.teacher import Teacher
from models.user import Role, User
from validators import valid_session, valid_args

manager_profile = Blueprint('manager_profile', __name__)

######################### STUDENTS #################################

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


######################### TEACHERS #################################

@manager_profile.route('/teacher_list', methods=['GET'])
def teacher_list():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_role = session['user_role']
    if user_role != Role.Admin:
        return redirect(url_for('main.index'))

    teachers = Teacher.get_all()
    data = []
    for t in teachers:
        full_name = ' '.join((t.last_name, t.first_name, t.patronymic))
        data.append({'id': t.id,
                     'name': full_name,
                     })

    return render_template('teacher_list.html', teachers=data)


@manager_profile.route('/edit_teacher_form/<id>', methods=['GET'])
def edit_teacher_form(id):
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    t = Teacher.get(id)
    if t is None:
        return '', 404

    user = User.get(id)
    if user is None:
        return '', 404

    return render_template('teacher_edit.html', teacher=t, user=user)


@manager_profile.route('/edit_teacher', methods=['POST'])
def edit_teacher():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    data = request.get_json(force=True)
    if not valid_args(data, 'id', 'first_name', 'last_name', 'patronymic'):
        return '', 500

    if not Teacher.update(id=data['id'],
                          first_name=data['first_name'],
                          last_name=data['last_name'],
                          patronymic=data['patronymic']
                          ):
        return '', 500

    return '', 200


@manager_profile.route('/create_teacher_form', methods=['GET'])
def create_teacher_form():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    empty_teacher = Teacher(0)
    empty_user = User(0)
    return render_template('teacher_edit.html', teacher=empty_teacher, user=empty_user)


@manager_profile.route('/create_teacher', methods=['POST'])
def create_teacher():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    data = request.get_json(force=True)
    if not valid_args(data, 'first_name', 'last_name', 'patronymic', 'login', 'password'):
        return '', 500

    ok = Teacher.create(login=data["login"],
                        password=hash_password(data['password']),
                        first_name=data['first_name'],
                        last_name=data['last_name'],
                        patronymic=data['patronymic']
                        )

    if not ok:
        return '', 500

    return '', 200


######################### specialities #################################

@manager_profile.route('/speciality_list', methods=['GET'])
def speciality_list():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_role = session['user_role']
    if user_role != Role.Admin:
        return redirect(url_for('main.index'))

    items = Speciality.get_all()
    data = []
    for item in items:
        data.append({'id': item.id, 'name': item.speciality_name})

    return render_template('speciality_list.html', items=data)


@manager_profile.route('/edit_speciality_form/<id>', methods=['GET'])
def edit_speciality_form(id):
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    item = Speciality.get(id)
    if item is None:
        return '', 404

    return render_template('speciality_edit.html', item=item)


@manager_profile.route('/edit_speciality', methods=['POST'])
def edit_speciality():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    data = request.get_json(force=True)
    if not valid_args(data, 'id', 'name'):
        return '', 500

    if not Speciality.update(id=data['id'], name=data['name']):
        return '', 500

    return '', 200


@manager_profile.route('/create_speciality_form', methods=['GET'])
def create_speciality_form():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    empty_item = Speciality(0)
    return render_template('speciality_edit.html', item=empty_item)


@manager_profile.route('/create_speciality', methods=['POST'])
def create_speciality():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    data = request.get_json(force=True)
    if not valid_args(data, 'name'):
        return '', 500

    ok = Speciality.create(name=data["name"])
    if not ok:
        return '', 500

    return '', 200


######################### disciplines #################################

@manager_profile.route('/discipline_list', methods=['GET'])
def discipline_list():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_role = session['user_role']
    if user_role != Role.Admin:
        return redirect(url_for('main.index'))

    items = Discipline.get_all()
    data = []
    for item in items:
        data.append({'id': item.id, 'name': item.discipline_name})

    return render_template('discipline_list.html', items=data)


@manager_profile.route('/edit_discipline_form/<id>', methods=['GET'])
def edit_discipline_form(id):
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    item = Discipline.get(id)
    if item is None:
        return '', 404

    return render_template('discipline_edit.html', item=item)


@manager_profile.route('/edit_discipline', methods=['POST'])
def edit_discipline():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    data = request.get_json(force=True)
    if not valid_args(data, 'id', 'name'):
        return '', 500

    if not Discipline.update(id=data['id'], name=data['name']):
        return '', 500

    return '', 200


@manager_profile.route('/create_discipline_form', methods=['GET'])
def create_discipline_form():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    empty_item = Discipline(0)
    return render_template('discipline_edit.html', item=empty_item)


@manager_profile.route('/create_discipline', methods=['POST'])
def create_discipline():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_role = session['user_role']
    if user_role != Role.Admin:
        return 'Доступ запрещен!', 403

    data = request.get_json(force=True)
    if not valid_args(data, 'name'):
        return 'Некорректные данные', 500

    ok = Discipline.create(name=data["name"])
    if not ok:
        return 'Ну удалось создать дисциплину', 500

    return 'Новая дисциплина создана!', 200
