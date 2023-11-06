import typer
import json
import datetime
import sqlite3

from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

console = Console()
from main import add_expense, view_expense
from database.db import create_user_database, create_user_config

app = typer.Typer(invoke_without_command=True)

@app.command()
def enter():
    """
        To enter monthly expense quote
    """
    current_total = float(Prompt.ask("Enter your current balance: "))
    budget = float(Prompt.ask("Enter the amount you want to spend: "))
    current_savings = current_total - budget
    needs = budget * 0.5
    wants = budget * 0.3
    savings = budget * 0.2

    with open('./database/config.json', 'r+') as config_file:
        config = json.load(config_file)
        user_name = config['USER_NAME']

    conn = sqlite3.connect('./database/'+user_name+'_config.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO config (MONTH_YEAR, CURRENT_TOTAL, CURRENT_SAVINGS, BUDGET, WANTS, NEEDS, SAVINGS) VALUES (?, ?, ?, ?, ?, ?, ?)", (datetime.date.today(), current_total, current_savings, budget, wants, needs, savings))
    conn.commit()
    console.print(f"Budget for this month: {budget}")
    conn.close()

@app.command()
def add(description: str, amount: float, date: str = None, tags: str = None):
    """
        To add expense to the database
    Args:
        description (str): description of the spending
        amount (float): the amount spent
        tags (str, optional): corresponding tag. Defaults to None.
        date (str, optional): date of the transaction. Defaults to None.
    """
    # add today's date if no input provided
    if date is None:
        date = datetime.date.today()

    # ask for user to choose tag if no input provided
    with open('./database/config.json', encoding='utf-8') as config_file:
        config = json.load(config_file)
    tag_data = config['TAGS']
    if tags is None:
        tag_chosen = Prompt.ask("Select tags", choices=tag_data, default=tag_data)
    else:
        tag_chosen = tags

    # call add_expense function from main.pyj
    add_expense(description, amount, date, tag_chosen)

@app.command()
def clear_inputs():
    """

    """
    conn = sqlite3.connect('money_management.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses")
    conn.commit()
    typer.echo("All inputs cleared.")

@app.command()
def view():
    view_expense()

@app.command()
def view_tags():
    with open('./database/config.json') as config_file:
        config = json.load(config_file)
    tags = config['TAGS']
    formatted_tags = "\n".join([f"- {tag}" for tag in tags])
    console.print(formatted_tags)

@app.callback()
def main(ctx: typer.Context):
    with open('./database/config.json') as config_file:
        data = json.load(config_file)
        FIRST_TIME = data['FIRST_TIME']
        USER_NAME = data['USER_NAME']

    if FIRST_TIME:
        print(Markdown("# Welcome to MoneyMax!"))
        print(Markdown("## Let's get started by creating a new account."))
        username = Prompt.ask("Enter a username: ")
        create_user_database(username)
        create_user_config(username)
        FIRST_TIME = False

        with open('./database/config.json', 'r+') as config_file:
            config = json.load(config_file)
            config['USER_NAME'] = username
            config['FIRST_TIME'] = False
            config_file.seek(0)
            json.dump(config, config_file)
            config_file.truncate()

    else:
        print(Markdown(f"# Welcome back, {USER_NAME}!"))

if __name__ == "__main__":
    app()


