import pyodbc
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime


#SQL Server Connection 
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=(localdb)\\MSSQLLocalDB;'
    'DATABASE=AttendanceTrackingDB;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

#Fetch Attendance by Student ID
def fetch_attendance_by_student(student_id):
    query = """
        SELECT s.name, c.course_name, a.date, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        JOIN courses c ON a.course_id = c.course_id
        WHERE a.student_id = ?
        ORDER BY a.date
    """
    cursor.execute(query, (student_id,))
    return cursor.fetchall()

#Fetch Attendance by Course ID
def fetch_attendance_by_course(course_id):
    query = """
        SELECT s.name, c.course_name, a.date, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.student_id
        JOIN courses c ON a.course_id = c.course_id
        WHERE a.course_id = ?
        ORDER BY a.date
    """
    cursor.execute(query, (course_id,))
    return cursor.fetchall()

#Report Generation 
def generate_pdf_by_student(student_id):
    data = fetch_attendance_by_student(student_id)
    if not data:
        print("No records found.")
        return

    student_name = data[0][0]
    filename = f"Attendance_Report_{student_name.replace(' ', '_')}.pdf"

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Attendance Report for {student_name}")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    table_data = [["Course", "Date", "Status"]]
    for row in data:
        table_data.append([row[1], row[2].strftime('%Y-%m-%d'), row[3]])

    table = Table(table_data, colWidths=[200, 150, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Position the table
    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height - 300)

    c.save()
    print(f"PDF generated: {filename}")

def generate_pdf_by_course(course_id):
    data = fetch_attendance_by_course(course_id)
    if not data:
        print("No records found.")
        return

    course_name = data[0][1]
    filename = f"Attendance_Report_{course_name.replace(' ', '_')}.pdf"

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Attendance Report for {course_name}")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 70, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    table_data = [["Student", "Date", "Status"]]
    for row in data:
        table_data.append([row[0], row[2].strftime('%Y-%m-%d'), row[3]])

    table = Table(table_data, colWidths=[200, 150, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Position the table
    table.wrapOn(c, width, height)
    table.drawOn(c, 50, height - 300)

    c.save()
    print(f"PDF generated: {filename}")
