from tkinter import messagebox
import customtkinter as ctk

import datetime

import sqlite3

# Function to clear the input fields
def clear_inputs(entry_list):
    for entry in entry_list:
        entry.delete(0, ctk.END)
    
def add_expense(description_entry, amount_entry, date_entry, cursor, conn):
    description = description_entry.get()
    amount = amount_entry.get()
    
    if date_entry.get() == "":
        date = datetime.date.today()
    else:
        date = date_entry.get()
        
    if description and amount:
        try:
            amount = float(amount)
            cursor.execute('INSERT INTO expenses (description, amount, date) VALUES (?, ?, ?)', (description, amount, date))
            conn.commit()
            clear_inputs([description_entry, amount_entry])
            messagebox.showinfo("Success", "Expense added successfully.")
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
    else:
        messagebox.showerror("Error", "Please enter both description and amount.")
