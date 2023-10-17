import customtkinter as ctk
from tkinter import messagebox

import sqlite3
import bcrypt
import os
import time

from utils.functions import create_user_database, clear_inputs
from core import main

# Create a main database to store user data
main_conn = sqlite3.connect('database/money_management.db')
main_cursor = main_conn.cursor()

# Create a table to store user accounts if it doesn't exist
main_cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
''')
main_conn.commit()
    
# Function to register a new user
def register_user():
    username = username_entry.get()
    password = password_entry.get()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    if username and password:
        main_cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        main_conn.commit()
        clear_inputs()
        messagebox.showinfo("Success", "User registered successfully.")
    else:
        messagebox.showerror("Error", "Please enter both username and password.")
    
# Function to authenticate a user
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username and password:
        main_cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
        user_data = main_cursor.fetchone()

        if user_data:
            user_id, hashed_password = user_data
            password_str = password.encode('utf-8')
            if bcrypt.checkpw(password_str, hashed_password):
                messagebox.showinfo("Success", "Login successful.")
                if not os.path.isfile('database/'+str(username)+'.db'):
                    create_user_database(username)
                clear_inputs([username_entry, password_entry])
                root.destroy() 
                main()  # Open the main application window
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        else:
            messagebox.showerror("Error", "Invalid username or password.")
    else:
        messagebox.showerror("Error", "Please enter both username and password.")


# Create the main window
root = ctk.CTk()
ctk.set_appearance_mode("dark")
root.title("Money Management App")
root.geometry("800x800")

# Create and configure labels and entry fields for login and registration
username_label = ctk.CTkLabel(root, text="Username:")
username_label.pack()
username_entry = ctk.CTkEntry(root)
username_entry.pack()

password_label = ctk.CTkLabel(root, text="Password:")
password_label.pack()
password_entry = ctk.CTkEntry(root, show='*')
password_entry.pack()

register_button = ctk.CTkButton(root, text="Register", command=register_user)
register_button.pack()

login_button = ctk.CTkButton(root, text="Login", command=login)
login_button.pack()

# Run the Tkinter main loop
root.mainloop()

# Close the main database connection when the app exits
main_conn.close()
