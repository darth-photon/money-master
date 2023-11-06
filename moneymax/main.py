import sqlite3
import datetime
import json

from rich import print
from rich.markdown import Markdown
from rich.console import Console
from rich.prompt import Prompt
console = Console()

from database.db import create_user_database


def add_expense(description: str, amount: float, date: str, tags: str) -> None:

    with open('./database/config.json') as config_file:
        config = json.load(config_file)
        user_name = config['USER_NAME']

    conn = sqlite3.connect('./database/' + user_name.lower() + '.db')
    cursor = conn.cursor()

    if date == "" or date == None:
        date = datetime.date.today()

    if description and amount:
        try:
            amount = float(amount)
            cursor.execute('INSERT INTO expenses (description, amount, date, tags) VALUES (?, ?, ?, ?)', (description, amount, date, tags))
            conn.commit()
            print()
            print("[bold green]Success[/bold green]: Expense added successfully.")
            print()

        except ValueError:
            console.print("[bold red]Error[/bold red]: Amount must be a number.")
    else:
        console.print("[bold red]Error[/bold red]: Please enter both description and amount.")

def view_expense():
    with open('./database/config.json') as config_file:
        config = json.load(config_file)
        user_name = config['USER_NAME']

    conn = sqlite3.connect('./database/' + user_name.lower() + '.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    if len(expenses) > 0:
        for expense in expenses:
            print(f"ID: {expense[0]}")
            print(f"Description: {expense[1]}")
            print(f"Amount: {expense[2]}")
            print(f"Date: {expense[3]}")
            print(f"Tags: {expense[4]}")
            print()
    else:
        print("No expenses found.")

if __name__ == "__main__":
    intro()