# graph_present_vs_absent.py

import pyodbc
import matplotlib.pyplot as plt

def plot_present_vs_absent(course_id):
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=(localdb)\\MSSQLLocalDB;'
        'DATABASE=AttendanceTrackingDB;'
        'Trusted_Connection=yes;'
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

    plt.figure(figsize=(6,6))
    plt.pie(counts, labels=statuses, autopct='%1.1f%%', startangle=140)
    plt.title(f"Present vs Absent for Course ID {course_id}")
    plt.axis("equal")
    plt.show()

# Run this file directly
if __name__ == "__main__":
    course_id = int(input("Enter course ID: "))
    plot_present_vs_absent(course_id)

