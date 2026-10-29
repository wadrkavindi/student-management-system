import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("students.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                course TEXT NOT NULL,
                marks REAL NOT NULL
            )
        """)

        self.connection.commit()

    def add_student(self, student):
        try:
            self.cursor.execute("""
                INSERT INTO students (student_id, name, email, course, marks)
                VALUES (?, ?, ?, ?, ?)
            """, (
                student.student_id,
                student.name,
                student.email,
                student.course,
                student.marks
            ))

            self.connection.commit()
            return True, "Student added successfully!"

        except sqlite3.IntegrityError:
            return False, "Student ID already exists!"

    def get_students(self):
        self.cursor.execute("SELECT * FROM students")
        return self.cursor.fetchall()

    def search_students(self, search_text):
        search_text = f"%{search_text}%"

        self.cursor.execute("""
            SELECT * FROM students
            WHERE student_id LIKE ?
               OR name LIKE ?
               OR email LIKE ?
        """, (
            search_text,
            search_text,
            search_text
        ))

        return self.cursor.fetchall()

    def update_student(self, student):
        self.cursor.execute("""
            UPDATE students
            SET name = ?, email = ?, course = ?, marks = ?
            WHERE student_id = ?
        """, (
            student.name,
            student.email,
            student.course,
            student.marks,
            student.student_id
        ))

        self.connection.commit()

        if self.cursor.rowcount == 0:
            return False, "Student not found!"

        return True, "Student updated successfully!"

    def delete_student(self, student_id):
        self.cursor.execute(
            "DELETE FROM students WHERE student_id = ?",
            (student_id,)
        )

        self.connection.commit()

        if self.cursor.rowcount == 0:
            return False, "Student not found!"

        return True, "Student deleted successfully!"

    def close(self):
        self.connection.close()
