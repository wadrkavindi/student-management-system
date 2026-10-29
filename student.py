class Student:
    def __init__(self, student_id, name, email, course, marks):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.course = course
        self.marks = marks

    def calculate_grade(self):
        if self.marks >= 75:
            return "A"
        elif self.marks >= 65:
            return "B"
        elif self.marks >= 50:
            return "C"
        else:
            return "F"
