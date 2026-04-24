import os
import sqlite3
from contextlib import contextmanager

DATABASE_URL = os.getenv("DATABASE_URL")
SQLITE_DB_NAME = "students.db"


def using_postgres():
    return bool(DATABASE_URL)


@contextmanager
def get_connection():
    if using_postgres():
        from psycopg import connect
        conn = connect(DATABASE_URL)
        try:
            yield conn
        finally:
            conn.close()
    else:
        conn = sqlite3.connect(SQLITE_DB_NAME)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()


def init_db():
    create_table_sql = """
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            student_code TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            department TEXT NOT NULL,
            level TEXT NOT NULL,
            study_hours REAL NOT NULL,
            tutorial_participation TEXT NOT NULL,
            attendance_rate REAL NOT NULL,
            ca_grade REAL NOT NULL,
            sleep_hours REAL NOT NULL,
            internet_quality TEXT NOT NULL,
            stress_level TEXT NOT NULL,
            final_grade REAL NOT NULL,
            admission_status TEXT NOT NULL
        )
    """

    if not using_postgres():
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_code TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                department TEXT NOT NULL,
                level TEXT NOT NULL,
                study_hours REAL NOT NULL,
                tutorial_participation TEXT NOT NULL,
                attendance_rate REAL NOT NULL,
                ca_grade REAL NOT NULL,
                sleep_hours REAL NOT NULL,
                internet_quality TEXT NOT NULL,
                stress_level TEXT NOT NULL,
                final_grade REAL NOT NULL,
                admission_status TEXT NOT NULL
            )
        """

    with get_connection() as conn:
        with conn.cursor() if using_postgres() else conn:
            if using_postgres():
                cur = conn.cursor()
                cur.execute(create_table_sql)
                conn.commit()
                cur.close()
            else:
                conn.execute(create_table_sql)
                conn.commit()


def insert_student(data):
    insert_sql = """
        INSERT INTO students (
            student_code,
            age,
            gender,
            department,
            level,
            study_hours,
            tutorial_participation,
            attendance_rate,
            ca_grade,
            sleep_hours,
            internet_quality,
            stress_level,
            final_grade,
            admission_status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    params = (
        data["student_code"],
        data["age"],
        data["gender"],
        data["department"],
        data["level"],
        data["study_hours"],
        data["tutorial_participation"],
        data["attendance_rate"],
        data["ca_grade"],
        data["sleep_hours"],
        data["internet_quality"],
        data["stress_level"],
        data["final_grade"],
        data["admission_status"]
    )

    if using_postgres():
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(insert_sql, params)
            conn.commit()
            cur.close()
    else:
        sqlite_sql = insert_sql.replace("%s", "?")
        with get_connection() as conn:
            conn.execute(sqlite_sql, params)
            conn.commit()


def get_all_students():
    query = "SELECT * FROM students ORDER BY id DESC"

    if using_postgres():
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query)
            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            cur.close()
            return [dict(zip(columns, row)) for row in rows]
    else:
        with get_connection() as conn:
            rows = conn.execute(query).fetchall()
            return rows