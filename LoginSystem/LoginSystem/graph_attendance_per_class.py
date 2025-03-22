# graph_attendance_per_class.py

import pyodbc
import matplotlib.pyplot as plt

def plot_attendance_per_class():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=(localdb)\\MSSQLLocalDB;'
        'DATABASE=AttendanceTrackingDB;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()

    query = """
        SELECT c.course_name, COUNT(*) as attendance_count
        FROM attendance a
        JOIN courses c ON a.course_id = c.course_id
        GROUP BY c.course_name
    """
    cursor.execute(query)
    results = cursor.fetchall()

    course_names = [row[0] for row in results]
    attendance_counts = [row[1] for row in results]

    plt.figure(figsize=(10,6))
    plt.bar(course_names, attendance_counts)
    plt.xlabel("Course")
    plt.ylabel("Attendance Count")
    plt.title("Total Attendance per Class")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Run this file directly
if __name__ == "__main__":
    plot_attendance_per_class()

