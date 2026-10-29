import tkinter as tk
from tkinter import ttk, messagebox

from database import Database
from student import Student


class StudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.database = Database()

        self.root.title("Student Management System")
        self.root.geometry("950x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#F4F6F7")

        self.create_input_fields()
        self.create_buttons()
        self.create_table()
        self.load_students()

    def create_input_fields(self):
        title_label = tk.Label(
            self.root,
            text="Student Management System",
            font=("Arial", 22, "bold"),
            bg="#F4F6F7",
            fg="#2C3E50"
        )
        title_label.pack(pady=15)

        input_frame = tk.Frame(self.root, padx=20, pady=10, bg="#F4F6F7")
        input_frame.pack(fill="x")

        label_style = {
            "font": ("Arial", 10, "bold"),
            "bg": "#F4F6F7"
        }
        entry_style = {
            "width": 25,
            "font": ("Arial", 11),
            "relief": "solid",
            "bd": 1
        }

        tk.Label(input_frame, text="Student ID", **label_style).grid(
            row=0, column=0, padx=10, pady=8
        )
        self.student_id_entry = tk.Entry(input_frame, **entry_style)
        self.student_id_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Name", **label_style).grid(
            row=0, column=2, padx=10, pady=8
        )
        self.name_entry = tk.Entry(input_frame, **entry_style)
        self.name_entry.grid(row=0, column=3)

        tk.Label(input_frame, text="Email", **label_style).grid(
            row=1, column=0, padx=10, pady=8
        )
        self.email_entry = tk.Entry(input_frame, **entry_style)
        self.email_entry.grid(row=1, column=1)

        tk.Label(input_frame, text="Course", **label_style).grid(
            row=1, column=2, padx=10, pady=8
        )
        self.course_entry = tk.Entry(input_frame, **entry_style)
        self.course_entry.grid(row=1, column=3)

        tk.Label(input_frame, text="Marks", **label_style).grid(
            row=2, column=0, padx=10, pady=8
        )
        self.marks_entry = tk.Entry(input_frame, **entry_style)
        self.marks_entry.grid(row=2, column=1)

        tk.Label(input_frame, text="Search", **label_style).grid(
            row=3, column=0, padx=10, pady=8
        )
        self.search_entry = tk.Entry(input_frame, **entry_style)
        self.search_entry.grid(row=3, column=1)

    def create_buttons(self):
        button_frame = tk.Frame(self.root, pady=10, bg="#F4F6F7")
        button_frame.pack()

        buttons = [
            ("Add Student", self.add_student, "#27AE60"),
            ("Update Student", self.update_student, "#2980B9"),
            ("Delete Student", self.delete_student, "#E74C3C"),
            ("Clear", self.clear_fields, "#7F8C8D"),
            ("Search", self.search_student, "#8E44AD"),
            ("Show All", self.load_students, "#16A085"),
        ]

        for column, (text, command, color) in enumerate(buttons):
            tk.Button(
                button_frame,
                text=text,
                width=15,
                command=command,
                bg=color,
                fg="white",
                font=("Arial", 10, "bold")
            ).grid(row=0, column=column, padx=5)

    def create_table(self):
        table_frame = tk.Frame(self.root, bg="#F4F6F7")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = ("ID", "Student ID", "Name", "Email", "Course", "Marks", "Grade")

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        widths = {
            "ID": 50,
            "Student ID": 100,
            "Name": 120,
            "Email": 180,
            "Course": 160,
            "Marks": 80,
            "Grade": 80,
        }
        for column in columns:
            self.tree.heading(
                column,
                text=column,
                command=lambda c=column: self.sort_table(c, False)
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.select_student)

    @staticmethod
    def calculate_grade(marks):
        if marks >= 75:
            return "A"
        if marks >= 65:
            return "B"
        if marks >= 50:
            return "C"
        return "F"

    def sort_table(self, column, reverse):
        data = []

        for item in self.tree.get_children(""):
            values = self.tree.item(item, "values")
            data.append((values, item))

        def sort_key(row):
            value = row[0][column_index]
            return value.lower() if isinstance(value, str) else value

        column_index = self.tree["columns"].index(column)

        try:
            data.sort(
                key=lambda row: sort_key(row),
                reverse=reverse
            )
        except (ValueError, TypeError):
            data.sort(
                key=lambda row: str(row[0][column_index]).lower(),
                reverse=reverse
            )

        for index, (_, item) in enumerate(data):
            self.tree.move(item, "", index)

        self.tree.heading(
            column,
            command=lambda: self.sort_table(column, not reverse)
        )

    def add_student(self):
        student_id = self.student_id_entry.get().strip()
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        course = self.course_entry.get().strip()
        marks_text = self.marks_entry.get().strip()

        if not all((student_id, name, email, course, marks_text)):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        try:
            marks = float(marks_text)
        except ValueError:
            messagebox.showerror("Error", "Marks must be a number.")
            return

        if not 0 <= marks <= 100:
            messagebox.showerror("Error", "Marks must be between 0 and 100.")
            return

        student = Student(student_id, name, email, course, marks)
        success, message = self.database.add_student(student)

        if success:
            messagebox.showinfo("Success", message)
            self.clear_fields()
            self.load_students()
        else:
            messagebox.showerror("Error", message)

    def update_student(self):
        student_id = self.student_id_entry.get().strip()
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        course = self.course_entry.get().strip()
        marks_text = self.marks_entry.get().strip()

        if not all((student_id, name, email, course, marks_text)):
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return

        try:
            marks = float(marks_text)
        except ValueError:
            messagebox.showerror("Error", "Marks must be a number.")
            return

        if not 0 <= marks <= 100:
            messagebox.showerror("Error", "Marks must be between 0 and 100.")
            return

        student = Student(student_id, name, email, course, marks)
        success, message = self.database.update_student(student)

        if success:
            messagebox.showinfo("Success", message)
            self.clear_fields()
            self.load_students()
        else:
            messagebox.showwarning("Warning", message)

    def delete_student(self):
        student_id = self.student_id_entry.get().strip()

        if not student_id:
            messagebox.showerror("Error", "Please select a student first.")
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this student?"
        )
        if not confirm:
            return

        success, message = self.database.delete_student(student_id)
        if success:
            messagebox.showinfo("Success", message)
            self.clear_fields()
            self.load_students()
        else:
            messagebox.showerror("Error", message)

    def load_students(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for student_data in self.database.get_students():
            marks = float(student_data[5])
            self.tree.insert(
                "",
                "end",
                values=(
                    student_data[0],
                    student_data[1],
                    student_data[2],
                    student_data[3],
                    student_data[4],
                    marks,
                    self.calculate_grade(marks)
                )
            )

    def select_student(self, event=None):
        selected_items = self.tree.selection()
        if not selected_items:
            return

        values = self.tree.item(selected_items[0], "values")
        self.clear_fields()

        self.student_id_entry.insert(0, values[1])
        self.name_entry.insert(0, values[2])
        self.email_entry.insert(0, values[3])
        self.course_entry.insert(0, values[4])
        self.marks_entry.insert(0, values[5])

    def search_student(self):
        search_text = self.search_entry.get().strip()
        if not search_text:
            messagebox.showwarning(
                "Warning",
                "Please enter a Student ID, Name, or Email."
            )
            return

        students = self.database.search_students(search_text)

        for item in self.tree.get_children():
            self.tree.delete(item)

        if not students:
            messagebox.showinfo("Search", "No student found.")
            return

        for student_data in students:
            marks = float(student_data[5])
            self.tree.insert(
                "",
                "end",
                values=(
                    student_data[0],
                    student_data[1],
                    student_data[2],
                    student_data[3],
                    student_data[4],
                    marks,
                    self.calculate_grade(marks)
                )
            )

    def clear_fields(self):
        for entry in (
            self.student_id_entry,
            self.name_entry,
            self.email_entry,
            self.course_entry,
            self.marks_entry,
            self.search_entry,
        ):
            entry.delete(0, tk.END)

        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def close_application(self):
        self.database.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentManagementSystem(root)
    root.protocol("WM_DELETE_WINDOW", app.close_application)
    root.mainloop()
