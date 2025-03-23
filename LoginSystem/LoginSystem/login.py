# 1. --- Imports ---
import tkinter as tk
from tkinter import messagebox
import pyodbc
from course_management import course_form_ui, show_courses
from student_management import open_student_manager
from Enrollment_UICode import open_enrollment_window, view_enrollments_by_course
from attendance_tracker import launch_attendance_tracker, view_attendance_records
from report_generator import generate_pdf_by_course, generate_pdf_by_student
from attendance_graphs import plot_attendance_per_class, plot_present_vs_absent

# 2. --- Database Connection ---
conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=(localdb)\MSSQLLocalDB;'
    r'DATABASE=AttendanceTrackingDB;'
    r'Trusted_Connection=yes;'
)
cursor = conn.cursor()

# 3. --- Functions ---
def authenticate_user():
    username = entry_username.get()
    password = entry_password.get()

    query = "SELECT * FROM Users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()

    if result:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        root.withdraw()
        open_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Setup Scrollabars
def setup_scrollbars(window):
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

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return scrollable_frame

# --- Open Dashboard ---
def open_dashboard():
    dashboard = tk.Toplevel()
    dashboard.title("Attendance Dashboard")
    dashboard.geometry("400x400")

    scrollable_frame = setup_scrollbars(dashboard)

    # --- PDF Report Popup ---
    def handle_generate_pdf():
        top = tk.Toplevel(dashboard)
        top.title("Generate Attendance Report")
        top.geometry("300x150")

        scrollable_frame = setup_scrollbars(top)

        tk.Label(scrollable_frame, text="Enter Student ID:").pack(pady=5)
        
        tk.Button(scrollable_frame, text="Student", command=handle_generate_pdf_by_student).pack(pady=5)
        tk.Button(scrollable_frame, text="Course", command=handle_generate_pdf_by_course).pack(pady=5)

    # --- PDF Report Popup for Student ---
    def handle_generate_pdf_by_student():
        top = tk.Toplevel(dashboard)
        top.title("Generate Attendance Report")
        top.geometry("300x150")

        scrollable_frame = setup_scrollbars(top)

        tk.Label(scrollable_frame, text="Enter Student ID:").pack(pady=5)
        id_entry = tk.Entry(scrollable_frame)
        id_entry.pack()

        def submit():
            try:
                student_id = int(id_entry.get())
                result = generate_pdf_by_student(student_id)
                if result:
                    tk.messagebox.showinfo("PDF Report", result)
                else:
                    tk.messagebox.showwarning("No Data", "No attendance records found.")
                top.destroy()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to generate report:\n{e}")

        tk.Button(scrollable_frame, text="Generate PDF", command=submit).pack(pady=10)
        

    # --- PDF Report Popup for Course ---
    def handle_generate_pdf_by_course():
        top = tk.Toplevel(dashboard)
        top.title("Generate Attendance Report by Course")
        top.geometry("300x150")

        scrollable_frame = setup_scrollbars(top)

        tk.Label(scrollable_frame, text="Enter Course ID:").pack(pady=5)
        id_entry = tk.Entry(scrollable_frame)
        id_entry.pack()

        def submit():
            try:
                course_id = int(id_entry.get())
                result = generate_pdf_by_course(course_id)
                if result:
                    tk.messagebox.showinfo("PDF Report", result)
                else:
                    tk.messagebox.showwarning("No Data", "No attendance records found.")
                top.destroy()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to generate report:\n{e}")

        tk.Button(scrollable_frame, text="Generate PDF", command=submit).pack(pady=10)

    # --- Dropdown for Course-based Graph ---
    def open_present_vs_absent_popup():
        top = tk.Toplevel(dashboard)
        top.title("Select Course")
        top.geometry("300x150")

        scrollable_frame = setup_scrollbars(top)

        tk.Label(scrollable_frame, text="Select Course:").pack(pady=5)

        cursor.execute("SELECT id, name FROM courses")
        courses = cursor.fetchall()
        course_map = {f"{row.name} (ID: {row.id})": row.id for row in courses}

        selected = tk.StringVar(top)
        selected.set(list(course_map.keys())[0])  # default value

        dropdown = tk.OptionMenu(scrollable_frame, selected, *course_map.keys())
        dropdown.pack()

        def submit():
            course_id = course_map[selected.get()]
            top.destroy()
            plot_present_vs_absent(course_id)

        tk.Button(scrollable_frame, text="Show Chart", command=submit).pack(pady=10)

    # --- Dashboard Buttons ---
    tk.Label(scrollable_frame, text="Welcome to the Dashboard!", font=("Arial", 14)).pack(pady=10)

    #tk.Button(scrollable_frame, text="View Students Present per Class", command=plot_attendance_per_class).pack(pady=5)
    tk.Button(scrollable_frame, text="Student Management", command=open_student_manager).pack(pady=5)
    tk.Button(scrollable_frame, text="Course Management", command=course_form_ui).pack(pady=5)
    tk.Button(scrollable_frame, text="Enroll Student", command=open_enrollment_window).pack(pady=5)
    tk.Button(scrollable_frame, text="Open Attendance Manager", command=open_attendance_manager).pack(pady=5)
    #tk.Button(scrollable_frame, text="View Attendance Records", command=view_attendance_records).pack(pady=5)
    tk.Button(scrollable_frame, text="View Attendance per Class", command=plot_attendance_per_class).pack(pady=5)
    tk.Button(scrollable_frame, text="View Present vs. Absent (Select Course)", command=open_present_vs_absent_popup).pack(pady=5)
    tk.Button(scrollable_frame, text="View Enrollments by Course", command=view_enrollments_by_course).pack(pady=5)
    tk.Button(scrollable_frame, text="View Courses", command=show_courses).pack(pady=5)
    tk.Button(scrollable_frame, text="Generate PDF Attendance Report", command=handle_generate_pdf).pack(pady=5)
    tk.Button(scrollable_frame, text="Logout", command=lambda: [dashboard.destroy(), root.quit()]).pack(pady=20)

def open_attendance_manager():
    launch_attendance_tracker()

# 4. --- GUI Login Form ---
root = tk.Tk()
root.title("Attendance Tracker - Login")
root.geometry("300x180")

tk.Label(root, text="Username").pack(pady=(20, 5))
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password").pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Login", command=authenticate_user).pack(pady=15)
tk.Button(root, text="Track Attendance", command=launch_attendance_tracker).pack(pady=10)

root.mainloop()
