import tkinter as tk
from tkinter import messagebox

accounts = [
    { "username": "sudev", "password": "123" },
    { "username": "sudev1", "password": "sudev1" },
]

def try_login():
    username = entry1.get()
    password = entry2.get()
    found = False
    for account in accounts:
        if username == account["username"] and password == account["password"]:
            found = True
            break
    if found: messagebox.showinfo("Success", f"Login successfull!\nWelcome {username}.")
    else:     messagebox.showerror("Denied", "Credentials don't match!")

window = tk.Tk()
window.geometry("300x150")
window.title("Login Panel")

label1 = tk.Label(window, text="Enter username: ")
label1.pack(pady=0)
entry1 = tk.Entry(window)
entry1.pack(pady=0)

label2 = tk.Label(window, text="Enter password: ")
label2.pack(pady=0)
entry2 = tk.Entry(window, show="*")
entry2.pack(pady=0)

submit_button = tk.Button(window, text="Login", command=try_login)
submit_button.pack(pady=10)

window.mainloop()