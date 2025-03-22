# dashboard.py

import tkinter as tk
from course_management import course_form_ui, show_courses

def open_attendance():
    window = tk.Toplevel()
    window.title("Attendance")
    window.geometry("300x200")
    tk.Label(window, text="Attendance functionality coming soon!").pack()

def dashboard():
    window = tk.Toplevel()
    window.title("Dashboard")
    window.geometry("400x300")

    tk.Label(window, text="Welcome!", font=("Arial", 16)).pack(pady=10)

    tk.Button(window, text="Attendance", command=open_attendance).pack(pady=10)

    tk.Button(window, text="Course Management", command=course_form_ui).pack(pady=10)

    tk.Button(dashboard, text="View Courses", command=show_courses).pack(pady=10)

    window.mainloop()
