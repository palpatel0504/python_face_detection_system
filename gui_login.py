import tkinter as tk
from tkinter import messagebox
import pandas as pd, sys

def validate(username, password):
    try:
        df = pd.read_excel("users.xlsx")
    except FileNotFoundError:
        messagebox.showerror("Error", "users.xlsx not found")
        return False
    return not df[(df.username==username)&(df.password==password)].empty

def on_login():
    u = entry_user.get().strip()
    p = entry_pass.get().strip()
    if validate(u, p):
        root.destroy()
        import face_recog   # launches the camera/recognition loop
        sys.exit(0)
    else:
        messagebox.showerror("Login Failed", "Invalid credentials")

root = tk.Tk()
root.title("Attendance Login")
root.resizable(False, False)
tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=5)
entry_user = tk.Entry(root); entry_pass = tk.Entry(root, show="*")
entry_user.grid(row=0, column=1, padx=10, pady=5)
entry_pass.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Login", width=20, command=on_login).grid(row=2, column=0, columnspan=2, pady=10)
root.mainloop()
