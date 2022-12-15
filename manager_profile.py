from flask import Blueprint, render_template, jsonify, request, session, url_for, redirect

from student import Student
from teacher import Teacher
from user import Role
from validators import valid_session

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
        data.append({'id': student.id,
                     'name': full_name,
                     'group': student.group_id,
                     'date': student.admission_date})

    return render_template('student_list.html', data=data)


@manager_profile.route('/student/<student_id>', methods=['GET'])
def student(student_id):
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    print(f'Edit student {student_id}')

    student = Student.get(student_id)
    if student is None:
        return '', 404

    return render_template('student_edit.html', student=student)


@manager_profile.route('/edit_student', methods=['POST'])
def edit_student():
    if not valid_session(session):
        return redirect(url_for('auth.login'))

    user_role = session['user_role']
    if user_role != Role.Admin:
        return '', 403

    data = request.get_json(force=True)
    student_id = data['id']
    student = Student.get(student_id)
    if student is None:
        return '', 404

    student.first_name = data['first_name']
    student.last_name = data['last_name']
    if not Student.update(student):
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

    return '', 200
