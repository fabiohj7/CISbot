import sqlite3

from . import config

db_path = config.DB_PATH

conn = sqlite3.connect(db_path)


def connect():

    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS questions (
            username TEXT,
            question TEXT
        )

    ''')


def get_question_by_user(username):
    query = '''
    SELECT question
    FROM questions
    '''
    return connect().execute(query).fetchall()


def remove_questions_by_user(username):
    query = '''
    DELETE FROM questions
    WHERE username = ?
    '''

    conn.execute(query, (username))
    conn.commit()


def get_users():
    query = '''
    SELECT username
    FROM questions
    '''

    user = conn.execute(query).fetchall()
    return [row[0] for row in user]


def add_users(username, question):
    query = '''
    INSERT INTO questions (username, question)
    VALUES (?, ?)
    '''
    conn.execute(query, (username, question))
    conn.commit()
