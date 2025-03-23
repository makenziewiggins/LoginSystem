# course_management.py

import tkinter as tk
from tkinter import messagebox
import pyodbc

# SQL Server connection
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=(localdb)\\MSSQLLocalDB;'  # <- Try this for LocalDB
    'DATABASE=AttendanceTrackingDB;'
    'Trusted_Connection=yes;'
)

cursor = conn.cursor()

# Function to insert a new course into the database
def add_course(name, description, course_number):
    try:
        cursor.execute("""
            INSERT INTO Courses (name, description, course_number)
            VALUES (?, ?, ?)
        """, name, description, course_number)
        conn.commit()
        return True
    except Exception as e:
        print("Error:", e)
        return False

# Edit Courses
def update_course(course_number, new_name, new_description):
    try:
        cursor.execute("""
            UPDATE Courses
            SET name = ?, description = ?
            WHERE course_number = ?
        """, new_name, new_description, course_number)
        conn.commit()
        return True
    except Exception as e:
        print("Error:", e)
        return False

#View courses 
def view_courses():
    try:
        cursor.execute("SELECT name, description, course_number FROM Courses")
        courses = cursor.fetchall()
        return courses
    except Exception as e:
        print("Error:", e)
        return []

# Show Courses
def show_courses():
    courses = view_courses()

    if not courses:
        messagebox.showinfo("No Data", "No courses available.")
        return

    window = tk.Toplevel()
    window.title("View Courses")
    window.geometry("500x500")

    tk.Label(window, text="Available Courses", font=("Arial", 14)).pack(pady=10)

    canvas = tk.Canvas(window)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for course in courses:
        frame = tk.Frame(scrollable_frame)
        frame.pack(fill="x", padx=10, pady=5)

        course_text = f"{course[0]} ({course[2]}): {course[1]}"
        tk.Label(frame, text=course_text, anchor="w", width=50).pack(side="left")

        tk.Button(frame, text="Edit", command=lambda c=course: open_edit_form(c)).pack(side="right")

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Button(window, text="Close", command=window.destroy).pack(pady=10)

# Edit Course Form
def open_edit_form(course):
    window = tk.Toplevel()
    window.title("Edit Course")
    window.geometry("400x250")

    tk.Label(window, text="Edit Course", font=("Arial", 14)).pack(pady=10)

    tk.Label(window, text="Course Name:").pack()
    name_entry = tk.Entry(window, width=40)
    name_entry.insert(0, course[0])
    name_entry.pack()

    tk.Label(window, text="Description:").pack()
    desc_entry = tk.Entry(window, width=40)
    desc_entry.insert(0, course[1])
    desc_entry.pack()

    def save_changes():
        new_name = name_entry.get()
        new_desc = desc_entry.get()
        course_number = course[2]

        if update_course(course_number, new_name, new_desc):
            messagebox.showinfo("Success", "Course updated successfully!")
            window.destroy()
        else:
            messagebox.showerror("Error", "Update failed.")

    tk.Button(window, text="Save Changes", command=save_changes).pack(pady=15)

# Course Management UI form
def course_form_ui():
    window = tk.Toplevel()
    window.title("Course Management")
    window.geometry("400x300")

    tk.Label(window, text="Course Name:").pack()
    name_entry = tk.Entry(window, width=40)
    name_entry.pack()

    tk.Label(window, text="Course Description:").pack()
    desc_entry = tk.Entry(window, width=40)
    desc_entry.pack()

    tk.Label(window, text="Course Number:").pack()
    number_entry = tk.Entry(window, width=40)
    number_entry.pack()

    def submit_course():
        name = name_entry.get()
        description = desc_entry.get()
        course_number = number_entry.get()

        if name and course_number:
            success = add_course(name, description, course_number)
            if success:
                messagebox.showinfo("Success", "Course added successfully!")
                name_entry.delete(0, tk.END)
                desc_entry.delete(0, tk.END)
                number_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Failed to add course.")
        else:
            messagebox.showwarning("Input Error", "Course name and number are required.")

    tk.Button(window, text="Add Course", command=submit_course).pack(pady=10)
