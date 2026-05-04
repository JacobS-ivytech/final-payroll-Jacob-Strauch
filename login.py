import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("ABC Company - Login")
root.geometry("700x600")
root.configure(bg="white")

#banner
header = tk.Frame(root, bg="lightskyblue", height=50)
header.pack(fill="x")

header.pack_propagate(False)

title = tk.Label(header, text="ABC Company", bg="lightskyblue", fg="black", font=("Arial", 18))
title.pack(side="left", padx=10)

def close_app():
    root.destroy()

close_btn = tk.Button(header, text="X", command=close_app)
close_btn.pack(side="right", padx=10, pady=10)

#title
tk.Label(root, text="Employee Login", font=("Arial", 16), bg="white").pack(pady=15)

#form
form = tk.Frame(root, bg="whitesmoke", padx=20, pady=20)
form.pack(pady=10)

#Email
tk.Label(form, text="Email address:", bg="whitesmoke").grid(row=0, column=0, sticky="w")
email_entry = tk.Entry(form, width=30)
email_entry.grid(row=1, column=0, pady=5)

#Password
tk.Label(form, text="Password:", bg="whitesmoke").grid(row=2, column=0, sticky="w")
password_entry = tk.Entry(form, show="*", width=30)
password_entry.grid(row=3, column=0, pady=5)

#radio buttons
user_type = tk.StringVar(value="employee")

tk.Label(form, text="Account Type:", bg="whitesmoke").grid(row=4, column=0, sticky="w", pady=(10, 0))

tk.Radiobutton(form, text="Employee", variable=user_type, value="employee", bg="whitesmoke").grid(row=5, column=0, sticky="w")
tk.Radiobutton(form, text="Admin", variable=user_type, value="admin", bg="whitesmoke").grid(row=6, column=0, sticky="w")

#submit button
def submit():
    print(email_entry.get(), password_entry.get(), user_type.get())

tk.Button(form, text="Submit", bg="lightskyblue", fg="black", command=submit).grid(row=7, column=0, pady=15)

root.mainloop()
