# attendance_graphs.py

import pyodbc
import matplotlib.pyplot as plt

def plot_attendance_per_class():
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=(localdb)\MSSQLLocalDB;'
        r'DATABASE=AttendanceTrackingDB;'
        r'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()

    query = """
        SELECT c.name, COUNT(*) as present_count
        FROM attendance a
        JOIN courses c ON a.course_id = c.id
        WHERE a.status = 'present'
        GROUP BY c.name
    """
    cursor.execute(query)
    results = cursor.fetchall()

    course_names = [row[0] for row in results]
    present_counts = [row[1] for row in results]

    plt.figure(figsize=(10, 6))
    plt.bar(course_names, present_counts, color='skyblue')
    plt.xlabel("Course")
    plt.ylabel("Number of Students Present")
    plt.title("Number of Students Present per Class")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_present_vs_absent(course_id):
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=(localdb)\MSSQLLocalDB;'
        r'DATABASE=AttendanceTrackingDB;'
        r'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()

    query = """
        SELECT status, COUNT(*) as count
        FROM attendance
        WHERE course_id = ?
        GROUP BY status
    """
    cursor.execute(query, (course_id,))
    results = cursor.fetchall()

    if not results:
        print("No attendance data found for this course.")
        return

    statuses = [row[0] for row in results]
    counts = [row[1] for row in results]

    plt.figure(figsize=(6, 6))
    plt.pie(counts, labels=statuses, autopct='%1.1f%%', startangle=140)
    plt.title(f"Present vs Absent for Course ID {course_id}")
    plt.axis("equal")
    plt.show()
