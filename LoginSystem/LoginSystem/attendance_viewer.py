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
    # Removed student ID and course ID input boxes
    tk.Label(window, text="Date:").grid(row=0, column=0, padx=5, pady=5)
    date_picker = DateEntry(window, width=16, date_pattern='yyyy-mm-dd')
    date_picker.grid(row=0, column=1)

    # === Treeview for Results ===
    tree = ttk.Treeview(window, columns=("ID", "Student", "Course", "Date", "Status"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Student", text="Student ID")
    tree.heading("Course", text="Course ID")
    tree.heading("Date", text="Date")
    tree.heading("Status", text="Status")
    tree.column("ID", width=50)

    # === Scrollbars ===
    v_scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=v_scrollbar.set)
    v_scrollbar.grid(row=2, column=4, sticky='ns')

    h_scrollbar = ttk.Scrollbar(window, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=h_scrollbar.set)
    h_scrollbar.grid(row=3, column=0, columnspan=4, sticky='ew')

    # === Configure grid to expand the Treeview ===
    tree.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')
    window.grid_rowconfigure(2, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(3, weight=1)

    # === Search Logic ===
    def search_records():
        tree.delete(*tree.get_children())  # Clear previous results

        query = """
            SELECT a.id, s.name, c.name, a.date, a.status
            FROM Attendance a
            JOIN Students s ON a.student_id = s.id
            JOIN Courses c ON a.course_id = c.id
            WHERE a.date = ?
        """
        params = [date_picker.get_date()]

        cursor.execute(query, params)
        results = cursor.fetchall()

        for row in results:
            tree.insert("", "end", values=row)

    # === Button to Search ===
    tk.Button(window, text="Search", command=search_records).grid(row=0, column=2, padx=10, pady=5)

# === Main Window ===
root = tk.Tk()
root.title("Attendance System")

tk.Button(root, text="View Attendance Records", command=view_attendance_records).pack(pady=20)

root.mainloop()