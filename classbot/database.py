import sqlite3

from . import config

db_path = config.DB_PATH


def connect():
    conn = sqlite3.connect(db_path)

    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            username TEXT,
            question TEXT,
            section TEXT
        )

    ''')
    conn.commit()
    return conn


def get_question_by_user(username):

    query = '''
    SELECT question
    FROM questions
    WHERE username = ?
    '''
    return connect().execute(query, (username)).fetchall()


def remove_questions_by_user(username):
    conn = connect()
    query = '''
    DELETE FROM questions
    WHERE username = ?
    '''

    conn.execute(query, (username, ))
    conn.commit()
    conn.close()


def get_users():

    conn = connect()
    query = '''
    SELECT username
    FROM questions
    '''

    user = conn.execute(query).fetchall()
    conn.close()
    return [row[0] for row in user]


def add_users(username, question):
    conn = connect()
    query = '''
    INSERT INTO questions (username, question)
    VALUES (?, ?)
    '''
    conn.execute(query, (username, question))
    conn.commit()
    conn.close()


def add_section(username, section):
    conn = connect()
    query = '''
    INSERT INTO questions (section)
    WHERE username = (?)
    VALUES (?)
    '''

    conn.execute(query, (username, section))
    conn.close()


def get_section_by_user(username):
    conn = connect()
    query = '''
    SELECT section
    FROM questions
    WHERE username = (?)
    '''
    return conn.execute(query, (username, )).fetchone()
    conn.close()
