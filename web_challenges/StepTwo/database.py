import sqlite3


def init_db():
    conn = sqlite3.connect('school_portal.db')
    c = conn.cursor()

    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (
                     id
                     INTEGER
                     PRIMARY
                     KEY
                     AUTOINCREMENT,
                     username
                     TEXT
                     UNIQUE
                     NOT
                     NULL,
                     password
                     TEXT
                     NOT
                     NULL,
                     full_name
                     TEXT
                     NOT
                     NULL,
                     date_of_birth
                     TEXT,
                     address
                     TEXT,
                     phone
                     TEXT,
                     role
                     TEXT
                     NOT
                     NULL
                     DEFAULT
                     'student'
                 )''')

    # Create certificates table
    c.execute('''CREATE TABLE IF NOT EXISTS certificates
    (
        id
        INTEGER
        PRIMARY
        KEY
        AUTOINCREMENT,
        user_id
        INTEGER
        NOT
        NULL,
        course_name
        TEXT
        NOT
        NULL,
        issue_date
        TEXT
        NOT
        NULL,
        certificate_data
        TEXT,
        FOREIGN
        KEY
                 (
        user_id
                 ) REFERENCES users
                 (
                     id
                 ))''')

    # Create absences table
    c.execute('''CREATE TABLE IF NOT EXISTS absences
    (
        id
        INTEGER
        PRIMARY
        KEY
        AUTOINCREMENT,
        student_id
        INTEGER
        NOT
        NULL,
        date
        TEXT
        NOT
        NULL,
        reason
        TEXT,
        FOREIGN
        KEY
                 (
        student_id
                 ) REFERENCES users
                 (
                     id
                 ))''')

    # Insert default admin user
    try:
        c.execute("INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
                  ('admin', 'admin123', 'Administrator', 'admin'))
    except sqlite3.IntegrityError:
        pass

    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect('school_portal.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return user


def create_user(username, password, full_name):
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)',
                     (username, password, full_name))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    conn.close()
    return success


def update_profile(user_id, date_of_birth, address, phone):
    conn = get_db_connection()
    conn.execute('UPDATE users SET date_of_birth = ?, address = ?, phone = ? WHERE id = ?',
                 (date_of_birth, address, phone, user_id))
    conn.commit()
    conn.close()


def add_certificate(user_id, course_name, issue_date, certificate_data):
    conn = get_db_connection()
    conn.execute('INSERT INTO certificates (user_id, course_name, issue_date, certificate_data) VALUES (?, ?, ?, ?)',
                 (user_id, course_name, issue_date, certificate_data))
    conn.commit()
    conn.close()


def get_user_certificates(user_id):
    conn = get_db_connection()
    certificates = conn.execute('SELECT * FROM certificates WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    return certificates


def add_absence(student_id, date, reason):
    conn = get_db_connection()
    conn.execute('INSERT INTO absences (student_id, date, reason) VALUES (?, ?, ?)',
                 (student_id, date, reason))
    conn.commit()
    conn.close()


def get_absences():
    conn = get_db_connection()
    absences = conn.execute('''
                            SELECT absences.*, users.username
                            FROM absences
                                     JOIN users ON absences.student_id = users.id
                            ''').fetchall()
    conn.close()
    return absences