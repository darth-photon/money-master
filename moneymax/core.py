import customtkinter as ctk
from CTkTable import *

import sqlite3
import os.path
import datetime
from PIL import Image, ImageTk

import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from database.db import create_user_database
from utils.functions import add_expense, clear_inputs

def add_window(cursor, conn):
    
    add_window = ctk.CTk()
    add_window.title("Add Expense")
    add_window.geometry("400x400")

    description_label = ctk.CTkLabel(add_window, text="Description:")
    description_label.place(x=50, y=70)
    description_entry = ctk.CTkEntry(add_window)
    description_entry.place(x=120, y=70)

    amount_label = ctk.CTkLabel(add_window, text="Amount:")
    amount_label.place(x=50, y=100)
    amount_entry = ctk.CTkEntry(add_window)
    amount_entry.place(x=120, y=100)

    
    date_label = ctk.CTkLabel(add_window, text="Date:")
    date_label.place(x=50, y=130)
    date_entry = ctk.CTkEntry(add_window)
    date_entry.place(x=120, y=130)
    
    add_button = ctk.CTkButton(add_window, text="Add Expense", command=lambda: add_expense(description_entry, amount_entry, date_entry, cursor, conn))
    add_button.pack()

    clear_button = ctk.CTkButton(add_window, text="Clear", command=lambda: clear_inputs([description_entry, amount_entry, date_entry]))
    clear_button.pack()

    add_window.mainloop()
 
        
def view(cursor):    
    def update_table(event):
        sort_options = {
            "Sort by earliest date": (True, False, False, False),
            "Sort by latest date": (False, True, False, False),
            "Sort by increasing amount": (False, False, True, False),
            "Sort by decreasing amount": (False, False, False, True)
        }
        SORT_BY_DATE_EARLIEST, SORT_BY_DATE_LATEST, SORT_BY_AMOUNT_INCREASING, SORT_BY_AMOUNT_DECREASING = sort_options.get(event, (False, False, False, False))
            
        cursor.execute("SELECT description, amount, date FROM expenses")
        rows = cursor.fetchall()
        header = ("Description", "Amount", "Date")
        
        if SORT_BY_DATE_EARLIEST:
            rows.sort(key=lambda x: datetime.datetime.strptime(x[2], '%Y-%m-%d'), reverse=True)
        if SORT_BY_DATE_LATEST:
            rows.sort(key=lambda x: datetime.datetime.strptime(x[2], '%Y-%m-%d'), reverse=False)  
        if SORT_BY_AMOUNT_DECREASING:
            rows.sort(key=lambda x: x[1], reverse=True)
        if SORT_BY_AMOUNT_INCREASING:
            rows.sort(key=lambda x: x[1], reverse=False)
        
        if SORT_BY_DATE_EARLIEST or SORT_BY_DATE_LATEST or SORT_BY_AMOUNT_DECREASING or SORT_BY_AMOUNT_INCREASING:        
            rows = list(rows)
            rows = [tuple((str(x[0]), float(x[1]), str(x[2]))) for x in rows]
            rows.insert(0, header)
            
            table = CTkTable(master=view_window, row=len(rows), column=3, values=[header], header_color="Blue", hover_color = "red"
                            ,corner_radius=10, color_phase="vertical")
            for i, values in enumerate(rows):
                for j in range(3):
                    table.insert(i, j, values[j])
                    
            table.grid(row=3, column=0) 
            
            # Create a figure and a set of subplots
            fig, ax = plt.subplots()
            
            # Convert rows data into a pandas DataFrame for easier manipulation
            df = pd.DataFrame(rows)
            df = df.drop(0) 
            df[2] = pd.to_datetime(df[2], errors='coerce')  # Convert the second column to datetime format
            df = df.dropna(subset=[2])  # Drop rows with invalid datetime values

            # Filter the DataFrame to consider only the last 10 days
            print(datetime.datetime.now() - datetime.timedelta(days=10))
            last_10_days = df[2] >= (datetime.datetime.now() - datetime.timedelta(days=10))
            df_filtered = df[last_10_days]
            
            # Group the DataFrame by the 'Date' column and sum the 'Amount' column
            df_agg = df_filtered.groupby(2)[1].sum().reset_index()
            
            f = Figure()
            a = f.add_subplot(111)
            a.bar(df_agg[2], df_agg[1])

            canvas = FigureCanvasTkAgg(f, master=view_window)
            canvas.draw()
            canvas.get_tk_widget().grid(row=3, column=1)
    
    def on_closing():
        view_window.destroy()
            
    view_window = ctk.CTk()
    view_window.grid_propagate(False) # Disable automatic resizing
    view_window.title("View Expenses")
    
    # Bind the on_closing function to the window's WM_DELETE_WINDOW protocol
    view_window.protocol("WM_DELETE_WINDOW", on_closing)

    optionmenu = ctk.CTkOptionMenu(view_window, values=["Sort by earliest data", "Sort by latest date", "Sort by increasing amount", "Sort by decreasing amount"],
                                         command=update_table)
    
    optionmenu.grid(row=0, column=0)
    optionmenu.set("Choose an option to sort")
    
    view_window.mainloop()

def exit_app(root):
    root.destroy()
        
def main():
    # Create a SQLite database or connect to an existing one
    username = "Shiva"
    if not os.path.isfile('./database/'+username+'.db'):
        create_user_database(username)

    conn = sqlite3.connect('./database/'+username+'.db')
    cursor = conn.cursor()

    # Create the main window
    root = ctk.CTk()
    root.title("Money Management App")
    root.geometry("500x300")
    
    
    title_label = ctk.CTkLabel(root, text="Budget Buddy", font=("Arial", 24))
    title_label.pack()
    title_label.place(x=150, y=50)
    
    
    add_button = ctk.CTkButton(root, text="Add", command= lambda: add_window(cursor, conn))
    add_button.pack()
    add_button.place(x=10, y=100)
    
    view_button = ctk.CTkButton(root, text="View", command=lambda: view(cursor))
    view_button.pack()
    view_button.place(x=170, y=100)
    
    exit_button = ctk.CTkButton(root, text="Exit", command=lambda: exit_app(root))
    exit_button.pack()
    exit_button.place(x=330, y=100)
        
    # Run the Tkinter main loop
    root.mainloop()

    # Close the database connection when the app exits
    conn.close()

if __name__ == "__main__":
    main()
    
