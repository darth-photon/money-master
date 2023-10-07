from tkinter import messagebox
import customtkinter as ctk

import sqlite3

# Function to clear the input fields
def clear_inputs(entry_list):
    for entry in entry_list:
        entry.delete(0, ctk.END)
    
def add_expense(description_entry, amount_entry, cursor, conn):
    description = description_entry.get()
    amount = amount_entry.get()
    if description and amount:
        try:
            amount = float(amount)
            cursor.execute('INSERT INTO expenses (description, amount) VALUES (?, ?)', (description, amount))
            conn.commit()
            clear_inputs([description_entry, amount_entry])
            messagebox.showinfo("Success", "Expense added successfully.")
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
    else:
        messagebox.showerror("Error", "Please enter both description and amount.")
        
def create_user_database(username):
    user_db_name = f"database/{username}.db"
    user_conn = sqlite3.connect(user_db_name)
    user_cursor = user_conn.cursor()

    user_cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL
        )
    ''')

    user_conn.commit()
    user_conn.close()
