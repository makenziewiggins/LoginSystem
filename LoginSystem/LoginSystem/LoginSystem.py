import tkinter as tk
from tkinter import messagebox
import mysql.connector

def authenticate_user():
    username = entry_username.get()
    password = entry_password.get()

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='admin',
            password='password123',
            database='AttendanceTrackingDB'
        )

        cursor = conn.cursor()
        query = "SELECT * FROM Users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Login Successful", f"Welcome, {username}!")
            root.destroy()
            # Open dashboard or next window here
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

# GUI Setup
root = tk.Tk()
root.title("Login System")

tk.Label(root, text="Username").grid(row=0, column=0, padx=10, pady=5)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Password").grid(row=1, column=0, padx=10, pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=5)

login_btn = tk.Button(root, text="Login", command=authenticate_user)
login_btn.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()

