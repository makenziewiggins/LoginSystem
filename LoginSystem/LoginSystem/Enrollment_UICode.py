import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

# SQL Server connection
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=(localdb)\\MSSQLLocalDB;'
    'DATABASE=AttendanceTrackingDB;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

def get_students():
    cursor.execute("SELECT id, name FROM Students")
    return cursor.fetchall()

def get_courses():
    cursor.execute("SELECT id, name FROM Courses")
    return cursor.fetchall()

def open_enrollment_window():
    window = tk.Toplevel()
    window.title("Enroll Student in Course")
    window.geometry("400x220")

    tk.Label(window, text="Select Student").pack(pady=5)
    student_dropdown = ttk.Combobox(window, width=50)
    student_dropdown.pack()

    tk.Label(window, text="Select Course").pack(pady=5)
    course_dropdown = ttk.Combobox(window, width=50)
    course_dropdown.pack()

    def enroll_student():
        selected_student = student_dropdown.get()
        selected_course = course_dropdown.get()

        if not selected_student or not selected_course:
            messagebox.showwarning("Missing Info", "Please select both student and course.")
            return

        student_id = selected_student.split(" - ")[0]
        course_id = selected_course.split(" - ")[0]

        try:
            cursor.execute("""
                SELECT 1 FROM Enrollments 
                WHERE student_id = ? AND course_id = ?
            """, student_id, course_id)
            if cursor.fetchone():
                messagebox.showinfo("Already Enrolled", "This student is already enrolled in the selected course.")
                return

            cursor.execute("INSERT INTO Enrollments (student_id, course_id) VALUES (?, ?)", student_id, course_id)
            conn.commit()
            messagebox.showinfo("Success", "Student enrolled in course.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enroll: {e}")

    tk.Button(window, text="Enroll", command=enroll_student).pack(pady=20)

    student_data = [f"{row[0]} - {row[1]}" for row in get_students()]
    course_data = [f"{row[0]} - {row[1]}" for row in get_courses()]
    student_dropdown['values'] = student_data
    course_dropdown['values'] = course_data

def view_enrollments_by_course():
    window = tk.Toplevel()
    window.title("View Enrollments by Course")
    window.geometry("450x350")

    tk.Label(window, text="Select Course", font=("Arial", 12)).pack(pady=5)
    course_combo = ttk.Combobox(window, width=50)
    course_combo.pack()

    result_frame = tk.Frame(window)
    result_frame.pack(pady=10, fill="both", expand=True)

    def show_enrolled_students():
        # Clear previous results
        for widget in result_frame.winfo_children():
            widget.destroy()

        selected = course_combo.get()
        if not selected:
            return

        course_id = selected.split(" - ")[0]

        try:
            cursor.execute("""
                SELECT s.name, s.email 
                FROM Enrollments e
                JOIN Students s ON e.student_id = s.id
                WHERE e.course_id = ?
            """, course_id)
            results = cursor.fetchall()

            if not results:
                tk.Label(result_frame, text="No students enrolled in this course.").pack()
                return

            for student in results:
                tk.Label(result_frame, text=f"{student.name} ({student.email})").pack(anchor="w")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(window, text="Show Enrolled Students", command=show_enrolled_students).pack(pady=10)

    # Load course dropdown
    course_data = [f"{row[0]} - {row[1]}" for row in get_courses()]
    course_combo['values'] = course_data
