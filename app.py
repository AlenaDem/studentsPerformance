import psycopg2
import psycopg2.extras
from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime

hostname = 'localhost'
database = 'testdb'
username = 'postgres'
pwd = 'Kak$delatKur$0vuyu???'
port_id = '5432'
conn = None
cur = None

try:
    with psycopg2.connect(
                host = hostname,
                dbname = database,
                user = username,
                password = pwd,
                port = port_id) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            #cur.execute('DROP TABLE IF EXISTS students')

            create_table = ''' CREATE TABLE IF NOT EXISTS specialities (
                                    id SERIAL PRIMARY KEY,
                                    speciality_name VARCHAR(64) NOT NULL)'''
            cur.execute(create_table)

            create_table = ''' CREATE TABLE IF NOT EXISTS disciplines (
                                    id SERIAL PRIMARY KEY,
                                    discipline_name VARCHAR(64) NOT NULL)'''
            cur.execute(create_table)

            create_table = ''' CREATE TABLE IF NOT EXISTS sp_disciplines (
                                    id SERIAL PRIMARY KEY,
                                    discipline_id INTEGER REFERENCES disciplines(id),
                                    speciality_id INTEGER REFERENCES specialities(id))'''
            cur.execute(create_table)

            create_table = ''' CREATE TABLE IF NOT EXISTS groups (
                                    id SERIAL PRIMARY KEY,
                                    speciality_id INTEGER REFERENCES specialities(id),
                                    course SMALLINT)'''
            cur.execute(create_table)

            create_table = ''' CREATE TABLE IF NOT EXISTS users (
                                    id SERIAL PRIMARY KEY,
                                    login VARCHAR(128) UNIQUE NOT NULL,
                                    password VARCHAR(256) NOT NULL,
                                    role SMALLINT NOT NULL)'''
            cur.execute(create_table)

            create_table = ''' CREATE TABLE IF NOT EXISTS students (
                                    id INTEGER PRIMARY KEY REFERENCES users(id),
                                    first_name VARCHAR(64) NOT NULL,
                                    last_name VARCHAR(64) NOT NULL,
                                    patronymic VARCHAR(64),
                                    admission_date SMALLINT,
                                    group_id INTEGER REFERENCES groups(id))'''
            cur.execute(create_table)

            create_table = ''' CREATE TABLE IF NOT EXISTS teachers (
                                    id INTEGER PRIMARY KEY REFERENCES users(id),
                                    first_name VARCHAR(64) NOT NULL,
                                    last_name VARCHAR(64) NOT NULL,
                                    patronymic VARCHAR(64))'''
            cur.execute(create_table)

            create_table = ''' CREATE TABLE IF NOT EXISTS tch_disciplines (
                                    id SERIAL PRIMARY KEY,
                                    teacher_id INTEGER REFERENCES teachers(id),
                                    discipline_id INTEGER REFERENCES disciplines(id))'''
            cur.execute(create_table)

            create_table = ''' CREATE TABLE IF NOT EXISTS grades (
                                    id SERIAL PRIMARY KEY,
                                    grade SMALLINT,
                                    datetime DATE,
                                    student_id INTEGER REFERENCES students(id),
                                    teacher_id INTEGER REFERENCES teachers(id),
                                    discipline_id INTEGER  REFERENCES disciplines(id))'''
            cur.execute(create_table)

            insert_script = 'INSERT INTO specialities (speciality_name) VALUES (%s)'
            insert_values = [('ИБС',), ('ИФБС',)]
            for record in insert_values:
                cur.execute(insert_script, record)

            insert_script = 'INSERT INTO groups (speciality_id, course) VALUES (%s, %s)'
            insert_values = [(1, 3,), (1, 4,), (2, 4,)]
            for record in insert_values:
                cur.execute(insert_script, record)

            insert_script = 'INSERT INTO users (login, password, role) VALUES (%s, %s, %s)'
            insert_values = [('st1', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 1,),
                             ('st2', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 1,),
                             ('st3', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 1,),
                             ('st4', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 1,),
                             ('tch1', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 1,),
                             ('tch2', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 1,),
                             ('tch3', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 1,),
                             ('tch4', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 1,),
                             ('tch5', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 1,),]
            for record in insert_values:
                cur.execute(insert_script, record)
            print('hello')

            insert_script = 'INSERT INTO students (id, last_name, first_name, patronymic, group_id, admission_date) ' \
                            'VALUES (%s, %s, %s, %s, %s, %s)'
            insert_values = [(1, 'Полякова', 'Алиса', 'Матвеевна', 1, 2020,),
                             (2, 'Чернов', 'Петр', 'Феликсович', 2, 2019,),
                             (3, 'Виноградова', 'Эрика', 'Давидовна', 2, 2019,),
                             (4, 'Овчинников', 'Юрий', 'Максимович', 3, 2019,)]
            for record in insert_values:
                cur.execute(insert_script, record)

            insert_script = 'INSERT INTO teachers (id, last_name, first_name, patronymic) VALUES (%s, %s, %s, %s)'
            insert_values = [(5, 'Фокина', 'Таисия', 'Геннадиевна',),
                             (6, 'Сергеева', 'София', 'Владимировна',),
                             (7, 'Владимиров', 'Степан', 'Андреевич',),
                             (8, 'Михайлова', 'Анна', 'Матвеевна',),
                             (9, 'Григорьев', 'Максим', 'Леонидович',)]
            for record in insert_values:
                cur.execute(insert_script, record)

            insert_script = 'INSERT INTO disciplines (discipline_name) VALUES (%s)'
            insert_values = [('Безопасность систем баз данных',),
                             ('Безопасность сетей ЭВМ',),
                             ('Безопасность жизнедеятельности',),
                             ('Основы управленческой деятельности',),
                             ('Параллельные системы и их программирование',),
                             ('Основы радиотехники',),
                             ('Вычислительная математика',),
                             ('Организация ЭВМ и вычислительных систем',)]
            for record in insert_values:
                cur.execute(insert_script, record)

            insert_script = 'INSERT INTO sp_disciplines (speciality_id, discipline_id) VALUES (%s, %s)'
            insert_values = [(1, 1,), (1, 2,), (2, 3,), (1, 4,), (2, 4,), (1, 5,), (2, 5,), (1, 6,), (1, 7,), (1, 8,)]
            for record in insert_values:
                cur.execute(insert_script, record)

            insert_script = 'INSERT INTO tch_disciplines (teacher_id, discipline_id) VALUES (%s, %s)'
            insert_values = [(5, 1,), (5, 2,), (5, 8,), (6, 6), (6, 7), (7, 3,), (8, 4,), (9, 5,)]
            for record in insert_values:
                cur.execute(insert_script, record)

            insert_script = 'INSERT INTO grades ' \
                            '(student_id, teacher_id, discipline_id, grade, datetime) ' \
                            'VALUES (%s, %s, %s, %s, %s)'
            insert_values = [(1, 6, 6, 5, '2021-06-29',),
                             (1, 6, 7, 4, '2022-01-18',),
                             (2, 5, 1, 5, '2021-07-01',),
                             (2, 6, 6, 4, '2021-06-30',),
                             (2, 6, 7, 4, '2021-01-18',),
                             (2, 9, 5, 4, '2022-07-03',),
                             (2, 6, 7, 3, '2021-07-02',),
                             (3, 8, 4, 5, '2021-07-02',),
                             (4, 9, 5, 5, '2022-01-15',)]
            for record in insert_values:
                cur.execute(insert_script, record)

            cur.execute('SELECT * FROM  students')
            for record in cur.fetchall():
                print(record['first_name'], record['last_name'])

except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()