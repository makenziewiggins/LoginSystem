import pyodbc
import pandas as pd

# Step 1: Connect to your database
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=(localdb)\\MSSQLLocalDB;'
    'DATABASE=AttendanceTrackingDB;'
    'Trusted_Connection=yes;'
)

# Step 2: List tables you want to inspect
tables = ["Users", "Students", "Courses", "Enrollments", "Attendance"]

# Step 3: Loop through and show each table
for table in tables:
    try:
        print(f"\n📋 {table} Table:")
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        print(df if not df.empty else "(No records found)")
    except Exception as e:
        print(f"Error reading {table}: {e}")

