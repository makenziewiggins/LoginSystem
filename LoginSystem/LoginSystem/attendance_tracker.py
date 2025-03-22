import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import pyodbc
from datetime import date

# ✅ Launch attendance input window
def launch_attendance_tracker():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=(localdb)\\MSSQLLocalDB;'
        'DATABASE=AttendanceTrackingDB;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    attendance_entries = []

    def validate_ids(student_id, course_id):
        cursor.execute("SELECT 1 FROM Students WHERE student_id = ?", student_id)
        student_exists = cursor.fetchone()
        cursor.execute("SELECT 1 FROM Courses WHERE course_id = ?", course_id)
        course_exists = cursor.fetchone()
        return student_exists and course_exists

    def check_duplicate(student_id, course_id, selected_date):
        cursor.execute("""
            SELECT 1 FROM Attendance
            WHERE student_id = ? AND course_id = ? AND date = ?
        """, (student_id, course_id, selected_date))
        return cursor.fetchone() is not None

    def add_attendance():
        student_id = student_id_entry.get()
        course_id = course_id_entry.get()
        status = status_var.get()
        selected_date = date_entry.get_date()

        if not student_id or not course_id:
            messagebox.showerror("Input Error", "Student ID and Course ID are required.")
            return

        if not validate_ids(student_id, course_id):
            messagebox.showerror("Validation Error", "Invalid Student ID or Course ID.")
            return

        if check_duplicate(student_id, course_id, selected_date):
            messagebox.showwarning("Duplicate Entry", "Attendance already recorded for this student on this date.")
            return

        attendance_entries.append((student_id, course_id, selected_date, status))
        messagebox.showinfo("Success", "Attendance added to batch list.")
        student_id_entry.delete(0, tk.END)
        course_id_entry.delete(0, tk.END)
        status_var.set("Present")

    def submit_batch():
        if not attendance_entries:
            messagebox.showwarning("Empty List", "No attendance records to submit.")
            return
        try:
            cursor.executemany("""
                INSERT INTO Attendance (student_id, course_id, date, status)
                VALUES (?, ?, ?, ?)
            """, attendance_entries)
            conn.commit()
            messagebox.showinfo("Success", "All attendance records submitted!")
            attendance_entries.clear()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    # === Tkinter Window ===
    tracker_window = tk.Toplevel()
    tracker_window.title("Attendance Tracker")

    tk.Label(tracker_window, text="Student ID:").grid(row=0, column=0, pady=5, sticky="e")
    student_id_entry = tk.Entry(tracker_window)
    student_id_entry.grid(row=0, column=1)

    tk.Label(tracker_window, text="Course ID:").grid(row=1, column=0, pady=5, sticky="e")
    course_id_entry = tk.Entry(tracker_window)
    course_id_entry.grid(row=1, column=1)

    tk.Label(tracker_window, text="Status:").grid(row=2, column=0, pady=5, sticky="e")
    status_var = tk.StringVar(tracker_window)
    status_var.set("Present")
    status_dropdown = tk.OptionMenu(tracker_window, status_var, "Present", "Absent")
    status_dropdown.grid(row=2, column=1)

    tk.Label(tracker_window, text="Date:").grid(row=3, column=0, pady=5, sticky="e")
    date_entry = DateEntry(tracker_window, width=18, background='darkblue',
                           foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    date_entry.grid(row=3, column=1)

    tk.Button(tracker_window, text="Add to List", command=add_attendance).grid(row=4, column=0, pady=10)
    tk.Button(tracker_window, text="Submit All", command=submit_batch).grid(row=4, column=1)


# ✅ View attendance records
def view_attendance_records():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=(localdb)\\MSSQLLocalDB;'
        'DATABASE=AttendanceTrackingDB;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()

    viewer = tk.Toplevel()
    viewer.title("View Attendance Records")
    viewer.geometry("600x400")

    tk.Label(viewer, text="Student ID:").grid(row=0, column=0)
    student_entry = tk.Entry(viewer)
    student_entry.grid(row=0, column=1)

    tk.Label(viewer, text="Course ID:").grid(row=0, column=2)
    course_entry = tk.Entry(viewer)
    course_entry.grid(row=0, column=3)

    tk.Label(viewer, text="Date:").grid(row=1, column=0)
    date_picker = DateEntry(viewer, date_pattern='yyyy-mm-dd')
    date_picker.grid(row=1, column=1)

    tree = ttk.Treeview(viewer, columns=("ID", "Student", "Course", "Date", "Status"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(viewer, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=3, column=4, sticky='ns')

    def search_records():
        tree.delete(*tree.get_children())
        query = "SELECT * FROM Attendance WHERE 1=1"
        params = []

        if student_entry.get():
            query += " AND student_id = ?"
            params.append(student_entry.get())

        if course_entry.get():
            query += " AND course_id = ?"
            params.append(course_entry.get())

        if date_picker.get():
            query += " AND date = ?"
            params.append(date_picker.get_date())

        cursor.execute(query, params)
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)

    tk.Button(viewer, text="Search", command=search_records).grid(row=1, column=3)
