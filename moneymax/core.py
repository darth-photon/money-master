import customtkinter as ctk

import sqlite3
import os.path

from database.db import create_database
from utils.functions import add_expense, clear_inputs

def add(root, cursor, conn):
    description_label = ctk.CTkLabel(root, text="Description:")
    description_label.pack()
    description_entry = ctk.CTkEntry(root)
    description_entry.pack()

    amount_label = ctk.CTkLabel(root, text="Amount:")
    amount_label.pack()
    amount_entry = ctk.CTkEntry(root)
    amount_entry.pack()

    add_button = ctk.CTkButton(root, text="Add Expense", command=lambda: add_expense(description_entry, amount_entry, cursor, conn))
    add_button.pack()

    clear_button = ctk.CTkButton(root, text="Clear", command=lambda: clear_inputs([description_entry, amount_entry]))
    clear_button.pack()

def view(root, cursor):
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    for row in rows:
        ctk.CTkLabel(root, text=row).pack()

def exit_app(root):
    root.destroy()
        
def main():
    # Create a SQLite database or connect to an existing one
    if not os.path.isfile('./database/Shiva.db'):
        create_database()

    conn = sqlite3.connect('./database/Shiva.db')
    cursor = conn.cursor()

    # Create the main window
    root = ctk.CTk()
    root.title("Money Management App")
    root.geometry("800x800")
    

    add_button = ctk.CTkButton(root, text="Add", command= lambda: add(root, cursor, conn))
    add_button.pack()

    view_button = ctk.CTkButton(root, text="View", command=lambda: view(root, cursor))
    view_button.pack()

    exit_button = ctk.CTkButton(root, text="Exit", command=lambda: exit_app(root))
    exit_button.pack()
        
    # Run the Tkinter main loop
    root.mainloop()

    # Close the database connection when the app exits
    conn.close()

if __name__ == "__main__":
    main()