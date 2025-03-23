import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import pyodbc

def view_attendance_records():
    # === DB Connection ===
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=(localdb)\\MSSQLLocalDB;'
        'DATABASE=AttendanceTrackingDB;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()

    # === GUI Window ===
    window = tk.Toplevel()
    window.title("View Attendance Records")
    window.geometry("600x400")

    # === Filter Form ===
    tk.Label(window, text="Student ID:").grid(row=0, column=0, padx=5, pady=5)
    student_entry = tk.Entry(window)
    student_entry.grid(row=0, column=1)

    tk.Label(window, text="Course ID:").grid(row=0, column=2, padx=5, pady=5)
    course_entry = tk.Entry(window)
    course_entry.grid(row=0, column=3)

    tk.Label(window, text="Date:").grid(row=1, column=0, padx=5, pady=5)
    date_picker = DateEntry(window, width=16, date_pattern='yyyy-mm-dd')
    date_picker.grid(row=1, column=1)

    # === Treeview for Results ===
    tree = ttk.Treeview(window, columns=("ID", "Student", "Course", "Date", "Status"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Student", text="Student ID")
    tree.heading("Course", text="Course ID")
    tree.heading("Date", text="Date")
    tree.heading("Status", text="Status")
    tree.column("ID", width=50)
    tree.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

    # === Scrollbar ===
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=3, column=4, sticky='ns')

    # === Search Logic ===
    def search_records():
        tree.delete(*tree.get_children())  # Clear previous results

        # query = "SELECT * FROM Attendance WHERE 1=1"
        # params = []
        qyery = """
            SELECT a.id, s.name, c.name, a.date, a.status
            FROM Attendance a
            JOIN Students s ON a.student_id = s.id
            JOIN Courses c ON a.course_id = c.id
            WHERE 1=1
        """
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
        results = cursor.fetchall()

        for row in results:
            tree.insert("", "end", values=row)

    # === Button to Search ===
    tk.Button(window, text="Search", command=search_records).grid(row=1, column=3, padx=10, pady=5)

