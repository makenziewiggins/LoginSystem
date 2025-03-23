import tkinter as tk
from tkinter import messagebox, filedialog
import pyodbc
import csv
from fpdf import FPDF

# Database Connection
conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=(localdb)\MSSQLLocalDB;'
    r'DATABASE=AttendanceTrackingDB;'
    r'Trusted_Connection=yes;'
)
cursor = conn.cursor()

def open_student_manager():
    print("Opening Student Manager")
    root = tk.Toplevel()
    root.title("Student Records")
    root.geometry("500x450")

    # Entry fields
    id_entry = tk.Entry(root)
    name_entry = tk.Entry(root)
    email_entry = tk.Entry(root)
    search_entry = tk.Entry(root)

    # Labels
    tk.Label(root, text="Student ID (for update/delete)").grid(row=0, column=0)
    id_entry.grid(row=0, column=1)
    tk.Label(root, text="Name").grid(row=1, column=0)
    name_entry.grid(row=1, column=1)
    tk.Label(root, text="Email").grid(row=2, column=0)
    email_entry.grid(row=2, column=1)
    tk.Label(root, text="Search by Name").grid(row=3, column=0)
    search_entry.grid(row=3, column=1)

    # CRUD Functions
    def create_student():
        name = name_entry.get()
        email = email_entry.get()

        try:
            cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            search_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def read_students():
        try:
            cursor.execute("SELECT id, name, email FROM Students")
            records = cursor.fetchall()
            output = "\n".join([f"{r.id} | {r.name} | {r.email}" for r in records])
            messagebox.showinfo("Student Records", output if output else "No records found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_student():
        sid = id_entry.get()
        name = name_entry.get()
        email = email_entry.get()

        try:
            cursor.execute("UPDATE Students SET name=?, email=? WHERE id=?", (name, email, sid))
            conn.commit()
            messagebox.showinfo("Success", "Student updated successfully!")
            search_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_student():
        sid = id_entry.get()
        try:
            cursor.execute("DELETE FROM Students WHERE id=?", (sid,))
            conn.commit()
            messagebox.showinfo("Success", "Student deleted successfully!")
            search_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_all_students_window(filter_name=None):
        try:
            if filter_name:
                cursor.execute("SELECT id, name, email FROM Students WHERE name LIKE ? ORDER BY name ASC", ('%' + filter_name + '%',))
            else:
                cursor.execute("SELECT id, name, email FROM Students ORDER BY name ASC")

            records = cursor.fetchall()

            for widget in results_frame.winfo_children():
                widget.destroy()

            for i, r in enumerate(records):
                tk.Label(results_frame, text=f"{r.id} | {r.name} | {r.email}", anchor="w").pack(fill="x", padx=5, pady=2)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_students(event=None):
        name_filter = search_entry.get()
        show_all_students_window(filter_name=name_filter)

    def export_to_csv():
        try:
            cursor.execute("SELECT id, name, email FROM Students ORDER BY name ASC")
            records = cursor.fetchall()

            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if not file_path:
                return

            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Email"])
                for r in records:
                    writer.writerow([r.id, r.name, r.email])

            messagebox.showinfo("Export Successful", f"Records exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_to_pdf():
        try:
            cursor.execute("SELECT id, name, email FROM Students ORDER BY name ASC")
            records = cursor.fetchall()

            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if not file_path:
                return

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Student Records", ln=True, align='C')

            for r in records:
                line = f"{r.id} | {r.name} | {r.email}"
                pdf.cell(200, 10, txt=line, ln=True)

            pdf.output(file_path)
            messagebox.showinfo("Export Successful", f"Records exported to {file_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Buttons
    tk.Button(root, text="Create", width=15, command=create_student).grid(row=4, column=0, pady=10)
    tk.Button(root, text="Read", width=15, command=read_students).grid(row=4, column=1)
    tk.Button(root, text="Update", width=15, command=update_student).grid(row=5, column=0)
    tk.Button(root, text="Delete", width=15, command=delete_student).grid(row=5, column=1)
    tk.Button(root, text="Export to CSV", width=15, command=export_to_csv).grid(row=6, column=0, pady=5)
    tk.Button(root, text="Export to PDF", width=15, command=export_to_pdf).grid(row=6, column=1, pady=5)

    # Results Area with Scrollbar
    results_frame = tk.Frame(root, bd=1, relief="sunken")
    results_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    scrollbar = tk.Scrollbar(results_frame)
    scrollbar.pack(side="right", fill="y")

    results_canvas = tk.Canvas(results_frame, yscrollcommand=scrollbar.set)
    results_canvas.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=results_canvas.yview)

    results_inner_frame = tk.Frame(results_canvas)
    results_canvas.create_window((0, 0), window=results_inner_frame, anchor="nw")

    def on_frame_configure(event):
        results_canvas.configure(scrollregion=results_canvas.bbox("all"))

    results_inner_frame.bind("<Configure>", on_frame_configure)

    root.grid_rowconfigure(7, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Real-time search binding
    search_entry.bind("<KeyRelease>", search_students)

    # Initial display
    show_all_students_window()
import tkinter as tk
from tkinter import messagebox, filedialog
import pyodbc
import csv
from fpdf import FPDF

# Database Connection
conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=(localdb)\MSSQLLocalDB;'
    r'DATABASE=AttendanceTrackingDB;'
    r'Trusted_Connection=yes;'
)
cursor = conn.cursor()

import tkinter as tk
from tkinter import messagebox, filedialog
import pyodbc
import csv
from fpdf import FPDF

# Database Connection
conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=(localdb)\MSSQLLocalDB;'
    r'DATABASE=AttendanceTrackingDB;'
    r'Trusted_Connection=yes;'
)
cursor = conn.cursor()

def open_student_manager():
    print("Opening Student Manager")
    root = tk.Toplevel()
    root.title("Student Records")
    root.geometry("500x450")

    # Entry fields
    id_entry = tk.Entry(root)
    name_entry = tk.Entry(root)
    email_entry = tk.Entry(root)
    search_entry = tk.Entry(root)

    # Labels
    tk.Label(root, text="Student ID (for update/delete)").grid(row=0, column=0)
    id_entry.grid(row=0, column=1)
    tk.Label(root, text="Name").grid(row=1, column=0)
    name_entry.grid(row=1, column=1)
    tk.Label(root, text="Email").grid(row=2, column=0)
    email_entry.grid(row=2, column=1)
    tk.Label(root, text="Search by Name").grid(row=3, column=0)
    search_entry.grid(row=3, column=1)

    # CRUD Functions
    def create_student():
        name = name_entry.get()
        email = email_entry.get()

        try:
            cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            search_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def read_students():
        try:
            cursor.execute("SELECT id, name, email FROM Students")
            records = cursor.fetchall()
            output = "\n".join([f"{r.id} | {r.name} | {r.email}" for r in records])
            messagebox.showinfo("Student Records", output if output else "No records found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_student():
        sid = id_entry.get()
        name = name_entry.get()
        email = email_entry.get()

        try:
            cursor.execute("UPDATE Students SET name=?, email=? WHERE id=?", (name, email, sid))
            conn.commit()
            messagebox.showinfo("Success", "Student updated successfully!")
            search_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_student():
        sid = id_entry.get()
        try:
            cursor.execute("DELETE FROM Students WHERE id=?", (sid,))
            conn.commit()
            messagebox.showinfo("Success", "Student deleted successfully!")
            search_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_all_students_window(filter_name=None):
        try:
            if filter_name:
                cursor.execute("SELECT id, name, email FROM Students WHERE name LIKE ? ORDER BY name ASC", ('%' + filter_name + '%',))
            else:
                cursor.execute("SELECT id, name, email FROM Students ORDER BY name ASC")

            records = cursor.fetchall()

            for widget in results_inner_frame.winfo_children():
                widget.destroy()

            for i, r in enumerate(records):
                tk.Label(results_inner_frame, text=f"{r.id} | {r.name} | {r.email}", anchor="w").pack(fill="x", padx=5, pady=2)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_students(event=None):
        name_filter = search_entry.get()
        show_all_students_window(filter_name=name_filter)

    def export_to_csv():
        try:
            cursor.execute("SELECT id, name, email FROM Students ORDER BY name ASC")
            records = cursor.fetchall()

            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if not file_path:
                return

            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Email"])
                for r in records:
                    writer.writerow([r.id, r.name, r.email])

            messagebox.showinfo("Export Successful", f"Records exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_to_pdf():
        try:
            cursor.execute("SELECT id, name, email FROM Students ORDER BY name ASC")
            records = cursor.fetchall()

            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if not file_path:
                return

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Student Records", ln=True, align='C')

            for r in records:
                line = f"{r.id} | {r.name} | {r.email}"
                pdf.cell(200, 10, txt=line, ln=True)

            pdf.output(file_path)
            messagebox.showinfo("Export Successful", f"Records exported to {file_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Buttons
    tk.Button(root, text="Create", width=15, command=create_student).grid(row=4, column=0, pady=10)
    tk.Button(root, text="Read", width=15, command=read_students).grid(row=4, column=1)
    tk.Button(root, text="Update", width=15, command=update_student).grid(row=5, column=0)
    tk.Button(root, text="Delete", width=15, command=delete_student).grid(row=5, column=1)
    tk.Button(root, text="Export to CSV", width=15, command=export_to_csv).grid(row=6, column=0, pady=5)
    tk.Button(root, text="Export to PDF", width=15, command=export_to_pdf).grid(row=6, column=1, pady=5)

    # Results Area with Scrollbar
    results_frame = tk.Frame(root, bd=1, relief="sunken")
    results_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    scrollbar = tk.Scrollbar(results_frame)
    scrollbar.pack(side="right", fill="y")

    results_canvas = tk.Canvas(results_frame, yscrollcommand=scrollbar.set)
    results_canvas.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=results_canvas.yview)

    results_inner_frame = tk.Frame(results_canvas)
    results_canvas.create_window((0, 0), window=results_inner_frame, anchor="nw")

    def on_frame_configure(event):
        results_canvas.configure(scrollregion=results_canvas.bbox("all"))

    results_inner_frame.bind("<Configure>", on_frame_configure)

    root.grid_rowconfigure(7, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Real-time search binding
    search_entry.bind("<KeyRelease>", search_students)

    # Initial display
    show_all_students_window()
import tkinter as tk
from tkinter import messagebox, filedialog
import pyodbc
import csv
from fpdf import FPDF

# Database Connection
conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=(localdb)\MSSQLLocalDB;'
    r'DATABASE=AttendanceTrackingDB;'
    r'Trusted_Connection=yes;'
)
cursor = conn.cursor()

import tkinter as tk
from tkinter import messagebox, filedialog
import pyodbc
import csv
from fpdf import FPDF

# Database Connection
conn = pyodbc.connect(
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=(localdb)\MSSQLLocalDB;'
    r'DATABASE=AttendanceTrackingDB;'
    r'Trusted_Connection=yes;'
)
cursor = conn.cursor()

def open_student_manager():
    print("Opening Student Manager")
    root = tk.Toplevel()
    root.title("Student Records")
    root.geometry("500x450")

    # Entry fields
    id_entry = tk.Entry(root)
    name_entry = tk.Entry(root)
    email_entry = tk.Entry(root)
    search_entry = tk.Entry(root)

    # Labels
    tk.Label(root, text="Student ID (for update/delete)").grid(row=0, column=0)
    id_entry.grid(row=0, column=1)
    tk.Label(root, text="Name").grid(row=1, column=0)
    name_entry.grid(row=1, column=1)
    tk.Label(root, text="Email").grid(row=2, column=0)
    email_entry.grid(row=2, column=1)
    tk.Label(root, text="Search by Name").grid(row=3, column=0)
    search_entry.grid(row=3, column=1)

    # CRUD Functions
    def create_student():
        name = name_entry.get()
        email = email_entry.get()

        try:
            cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            search_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def read_students():
        try:
            cursor.execute("SELECT id, name, email FROM Students ORDER BY id ASC")
            records = cursor.fetchall()
            output = "\n".join([f"{r.id} | {r.name} | {r.email}" for r in records])
            messagebox.showinfo("Student Records", output if output else "No records found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_student():
        sid = id_entry.get()
        name = name_entry.get()
        email = email_entry.get()

        try:
            cursor.execute("UPDATE Students SET name=?, email=? WHERE id=?", (name, email, sid))
            conn.commit()
            messagebox.showinfo("Success", "Student updated successfully!")
            search_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_student():
        sid = id_entry.get()
        try:
            cursor.execute("DELETE FROM Students WHERE id=?", (sid,))
            conn.commit()
            messagebox.showinfo("Success", "Student deleted successfully!")
            search_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_all_students_window(filter_name=None):
        try:
            if filter_name:
                cursor.execute("SELECT id, name, email FROM Students WHERE name LIKE ? ORDER BY id ASC", ('%' + filter_name + '%',))
            else:
                cursor.execute("SELECT id, name, email FROM Students ORDER BY id ASC")

            records = cursor.fetchall()

            for widget in results_inner_frame.winfo_children():
                widget.destroy()

            for i, r in enumerate(records):
                tk.Label(results_inner_frame, text=f"{r.id} | {r.name} | {r.email}", anchor="w").pack(fill="x", padx=5, pady=2)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_students(event=None):
        name_filter = search_entry.get()
        show_all_students_window(filter_name=name_filter)

    def export_to_csv():
        try:
            cursor.execute("SELECT id, name, email FROM Students ORDER BY id ASC")
            records = cursor.fetchall()

            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if not file_path:
                return

            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Email"])
                for r in records:
                    writer.writerow([r.id, r.name, r.email])

            messagebox.showinfo("Export Successful", f"Records exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_to_pdf():
        try:
            cursor.execute("SELECT id, name, email FROM Students ORDER BY id ASC")
            records = cursor.fetchall()

            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if not file_path:
                return

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Student Records", ln=True, align='C')

            for r in records:
                line = f"{r.id} | {r.name} | {r.email}"
                pdf.cell(200, 10, txt=line, ln=True)

            pdf.output(file_path)
            messagebox.showinfo("Export Successful", f"Records exported to {file_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Buttons
    tk.Button(root, text="Create", width=15, command=create_student).grid(row=4, column=0, pady=10)
    tk.Button(root, text="Read", width=15, command=read_students).grid(row=4, column=1)
    tk.Button(root, text="Update", width=15, command=update_student).grid(row=5, column=0)
    tk.Button(root, text="Delete", width=15, command=delete_student).grid(row=5, column=1)
    tk.Button(root, text="Export to CSV", width=15, command=export_to_csv).grid(row=6, column=0, pady=5)
    tk.Button(root, text="Export to PDF", width=15, command=export_to_pdf).grid(row=6, column=1, pady=5)

    # Results Area with Scrollbar
    results_frame = tk.Frame(root, bd=1, relief="sunken")
    results_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    scrollbar = tk.Scrollbar(results_frame)
    scrollbar.pack(side="right", fill="y")

    results_canvas = tk.Canvas(results_frame, yscrollcommand=scrollbar.set)
    results_canvas.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=results_canvas.yview)

    results_inner_frame = tk.Frame(results_canvas)
    results_canvas.create_window((0, 0), window=results_inner_frame, anchor="nw")

    def on_frame_configure(event):
        results_canvas.configure(scrollregion=results_canvas.bbox("all"))

    results_inner_frame.bind("<Configure>", on_frame_configure)

    root.grid_rowconfigure(7, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Real-time search binding
    search_entry.bind("<KeyRelease>", search_students)

    # Initial display
    show_all_students_window()
def open_student_manager():
    print("Opening Student Manager")
    root = tk.Toplevel()
    root.title("Student Records")
    root.geometry("500x450")

    # Entry fields
    id_entry = tk.Entry(root)
    name_entry = tk.Entry(root)
    email_entry = tk.Entry(root)
    search_entry = tk.Entry(root)

    # Labels
    tk.Label(root, text="Student ID (for update/delete)").grid(row=0, column=0)
    id_entry.grid(row=0, column=1)
    tk.Label(root, text="Name").grid(row=1, column=0)
    name_entry.grid(row=1, column=1)
    tk.Label(root, text="Email").grid(row=2, column=0)
    email_entry.grid(row=2, column=1)
    tk.Label(root, text="Search by Name").grid(row=3, column=0)
    search_entry.grid(row=3, column=1)

    # CRUD Functions
    def create_student():
        name = name_entry.get()
        email = email_entry.get()

        try:
            cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            search_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def read_students():
        try:
            cursor.execute("SELECT id, name, email FROM Students")
            records = cursor.fetchall()
            output = "\n".join([f"{r.id} | {r.name} | {r.email}" for r in records])
            messagebox.showinfo("Student Records", output if output else "No records found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_student():
        sid = id_entry.get()
        name = name_entry.get()
        email = email_entry.get()

        try:
            cursor.execute("UPDATE Students SET name=?, email=? WHERE id=?", (name, email, sid))
            conn.commit()
            messagebox.showinfo("Success", "Student updated successfully!")
            search_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_student():
        sid = id_entry.get()
        try:
            cursor.execute("DELETE FROM Students WHERE id=?", (sid,))
            conn.commit()
            messagebox.showinfo("Success", "Student deleted successfully!")
            search_students()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_all_students_window(filter_name=None):
        try:
            if filter_name:
                cursor.execute("SELECT id, name, email FROM Students WHERE name LIKE ? ORDER BY name ASC", ('%' + filter_name + '%',))
            else:
                cursor.execute("SELECT id, name, email FROM Students ORDER BY name ASC")

            records = cursor.fetchall()

            for widget in results_inner_frame.winfo_children():
                widget.destroy()

            for i, r in enumerate(records):
                tk.Label(results_inner_frame, text=f"{r.id} | {r.name} | {r.email}", anchor="w").pack(fill="x", padx=5, pady=2)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_students(event=None):
        name_filter = search_entry.get()
        show_all_students_window(filter_name=name_filter)

    def export_to_csv():
        try:
            cursor.execute("SELECT id, name, email FROM Students ORDER BY name ASC")
            records = cursor.fetchall()

            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if not file_path:
                return

            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Name", "Email"])
                for r in records:
                    writer.writerow([r.id, r.name, r.email])

            messagebox.showinfo("Export Successful", f"Records exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def export_to_pdf():
        try:
            cursor.execute("SELECT id, name, email FROM Students ORDER BY name ASC")
            records = cursor.fetchall()

            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if not file_path:
                return

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Student Records", ln=True, align='C')

            for r in records:
                line = f"{r.id} | {r.name} | {r.email}"
                pdf.cell(200, 10, txt=line, ln=True)

            pdf.output(file_path)
            messagebox.showinfo("Export Successful", f"Records exported to {file_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Buttons
    tk.Button(root, text="Create", width=15, command=create_student).grid(row=4, column=0, pady=10)
    tk.Button(root, text="Read", width=15, command=read_students).grid(row=4, column=1)
    tk.Button(root, text="Update", width=15, command=update_student).grid(row=5, column=0)
    tk.Button(root, text="Delete", width=15, command=delete_student).grid(row=5, column=1)
    tk.Button(root, text="Export to CSV", width=15, command=export_to_csv).grid(row=6, column=0, pady=5)
    tk.Button(root, text="Export to PDF", width=15, command=export_to_pdf).grid(row=6, column=1, pady=5)

    # Results Area with Scrollbar
    results_frame = tk.Frame(root, bd=1, relief="sunken")
    results_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    scrollbar = tk.Scrollbar(results_frame)
    scrollbar.pack(side="right", fill="y")

    results_canvas = tk.Canvas(results_frame, yscrollcommand=scrollbar.set)
    results_canvas.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=results_canvas.yview)

    results_inner_frame = tk.Frame(results_canvas)
    results_canvas.create_window((0, 0), window=results_inner_frame, anchor="nw")

    def on_frame_configure(event):
        results_canvas.configure(scrollregion=results_canvas.bbox("all"))

    results_inner_frame.bind("<Configure>", on_frame_configure)

    root.grid_rowconfigure(7, weight=1)
    root.grid_columnconfigure(1, weight=1)

    # Real-time search binding
    search_entry.bind("<KeyRelease>", search_students)

    # Initial display
    show_all_students_window()
