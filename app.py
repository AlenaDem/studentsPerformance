import logging
import sys

import psycopg2
import psycopg2.extras
from flask import Flask
from config import hostname, database, username, pwd, port_id

conn = None
cur = None

app = Flask(__name__)

def init_logger():
    fileHandler = logging.FileHandler("log.txt")

    format = logging.Formatter('%(asctime)s %(levelname)s - %(message)s')
    fileHandler.setFormatter(format)

    app.logger.addHandler(fileHandler)
    app.logger.setLevel(logging.DEBUG)


def init_db():
    try:
        with psycopg2.connect(
                host=hostname,
                dbname=database,
                user=username,
                password=pwd,
                port=port_id) as conn:

            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

                # cur.execute('DROP TABLE IF EXISTS students')

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

                create_table = ''' CREATE TABLE IF NOT EXISTS st_groups (
                                        id SERIAL PRIMARY KEY,
                                        speciality_id INTEGER REFERENCES specialities(id),
                                        course SMALLINT,
                                        group_name VARCHAR(32))'''
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
                                        group_id INTEGER REFERENCES st_groups(id))'''
                cur.execute(create_table)

                create_table = ''' CREATE TABLE IF NOT EXISTS teachers (
                                        id INTEGER PRIMARY KEY REFERENCES users(id),
                                        first_name VARCHAR(64) NOT NULL,
                                        last_name VARCHAR(64) NOT NULL,
                                        patronymic VARCHAR(64))'''
                cur.execute(create_table)

                create_table = ''' CREATE TABLE IF NOT EXISTS group_disciplines (
                                        id SERIAL PRIMARY KEY,
                                        academic_year SMALLINT,
                                        semester SMALLINT,
                                        discipline_id INTEGER REFERENCES disciplines(id),
                                        teacher_id INTEGER REFERENCES teachers(id),
                                        group_id INTEGER REFERENCES st_groups(id))'''
                cur.execute(create_table)

                create_table = ''' CREATE TABLE IF NOT EXISTS grades (
                                        id SERIAL PRIMARY KEY,
                                        grade SMALLINT,
                                        datetime DATE NOT NULL DEFAULT CURRENT_DATE,
                                        academic_year SMALLINT,
                                        semester SMALLINT,
                                        student_id INTEGER REFERENCES students(id),
                                        teacher_id INTEGER REFERENCES teachers(id),
                                        discipline_id INTEGER  REFERENCES disciplines(id))'''
                cur.execute(create_table)

                create_table = ''' CREATE TABLE IF NOT EXISTS otp (
                                        id INTEGER PRIMARY KEY REFERENCES users(id),
                                        secret VARCHAR(64) NOT NULL)'''
                cur.execute(create_table)

                insert_script = 'INSERT INTO specialities (speciality_name) VALUES (%s)'
                insert_values = [('ИБС',), ('ИФБС',)]
                for record in insert_values:
                    cur.execute(insert_script, record)

                insert_script = 'INSERT INTO st_groups (speciality_id, course, group_name) VALUES (%s, %s, %s)'
                insert_values = [(1, 3, 'ИБС-31'), (1, 4, 'ИБС-41'), (2, 4, 'ИФБС-41')]
                for record in insert_values:
                    cur.execute(insert_script, record)

                insert_script = 'INSERT INTO users (login, password, role) VALUES (%s, %s, %s)'
                insert_values = [('st1', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 1,),
                                 ('st2', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 1,),
                                 ('st3', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 1,),
                                 ('st4', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 1,),
                                 ('tch1', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 2,),
                                 ('tch2', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 2,),
                                 ('tch3', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 2,),
                                 ('tch4', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 2,),
                                 ('tch5', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 2,),
                                 ('root', 'df293094f3944b28571ab6e3de56237289a36ccccb38ee049ccc0f2838d0735a', 3,), ]
                for record in insert_values:
                    cur.execute(insert_script, record)

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
                insert_values = [(1, 1,), (1, 2,), (2, 3,), (1, 4,), (2, 4,), (1, 5,), (2, 5,), (1, 6,), (1, 7,),
                                 (1, 8,)]
                for record in insert_values:
                    cur.execute(insert_script, record)

                insert_script = 'INSERT INTO group_disciplines ' \
                                '(academic_year, semester, teacher_id, discipline_id, group_id) ' \
                                'VALUES (%s, %s, %s, %s, %s)'
                insert_values = [(2020, 2, 6, 6, 1,), (2021, 1, 6, 7, 1,), (2020, 2, 5, 1, 2,),
                                 (2020, 2, 6, 6, 2,), (2020, 1, 6, 7, 2,), (2021, 2, 9, 5, 2,),
                                 (2020, 2, 6, 7, 2,), (2020, 2, 8, 4, 2,), (2021, 1, 9, 5, 3,)]
                for record in insert_values:
                    cur.execute(insert_script, record)

                insert_script = 'INSERT INTO grades ' \
                                '(student_id, teacher_id, discipline_id, grade, datetime, academic_year, semester) ' \
                                'VALUES (%s, %s, %s, %s, %s, %s, %s)'
                insert_values = [(1, 6, 6, 5, '2021-06-29', 2020, 2,),
                                 (1, 6, 7, 4, '2022-01-18', 2021, 1,),
                                 (2, 5, 1, 5, '2021-07-01', 2020, 2,),
                                 (2, 6, 6, 4, '2021-06-30', 2020, 2,),
                                 (2, 6, 7, 4, '2021-01-18', 2020, 1,),
                                 (2, 9, 5, 4, '2022-07-03', 2021, 2,),
                                 (2, 6, 7, 3, '2021-07-02', 2020, 2,),
                                 (3, 8, 4, 5, '2021-07-02', 2020, 2,),
                                 (4, 9, 5, 5, '2022-01-15', 2021, 1)]
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
