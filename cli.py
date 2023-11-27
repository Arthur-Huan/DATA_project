import sqlite3
import typer
from typing_extensions import Annotated
from typing import Optional

from data_format_checks import *


app = typer.Typer()


def init_cursor(database_name):
    con = sqlite3.connect(database_name, timeout=120)
    cur = con.cursor()
    return cur


@app.command()
def register():
    cur = init_cursor("twitter_like.db")

    # Prompt for a new username, and check it
    username = typer.prompt("Enter new username")
    username_validity = username_check(username, cur)
    while username_validity != -1:
        if username_validity == 1:
            typer.echo("Length of username should be between 2 to 32 characters.")
        elif username_validity == 2:
            typer.echo("Username contains invalid characters. Only letters, numbers, and underscores are allowed.")
        elif username_validity == 3:
            typer.echo("Underscores should not be at the start of end of a username.")
        elif username_validity == 4:
            typer.echo("Username already in use.")
        else:
            typer.echo("Unexpected username formatting issue, please file a bug report.")
        # Prompt user for a new username
        username = typer.prompt("Enter new username")
        username_validity = username_check(username, cur)

    def input_new_password(
            password: Annotated[str, typer.Option(prompt=True, confirmation_prompt=True, hide_input=True)],):
        typer.echo(password)

    typer.run(input_new_password)


if __name__ == "__main__":
    app()
