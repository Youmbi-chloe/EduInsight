import sqlite3

DB_NAME = "students.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
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
    """)

    conn.commit()
    conn.close()

def insert_student(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
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
    ))

    conn.commit()
    conn.close()

def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students ORDER BY id DESC")
    students = cursor.fetchall()

    conn.close()
    return students