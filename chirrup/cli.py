from typing import Optional

import typer

from chirrup import __version__, __app_name__, __database_path__
from chirrup.backend import *

app = typer.Typer()


@app.command()
def register():
    register_user(cursor)


@app.command()
def login():
    username = login_user(cursor)
    if username:  # If login is successful, show additional commands
        # ========================
        # 3.8 - User Friendly Menu System ###
        # ========================
        typer.echo("Welcome, {}!".format(username))
        typer.echo("1. Post a new tweet")
        typer.echo("2. View your timeline")
        typer.echo("3. Like a tweet")
        typer.echo("4. View likes on a tweet")
        typer.echo("5. Add a comment to a tweet")
        typer.echo("6. Follow a user")
        typer.echo("7. Unfollow a user")

        choice = typer.prompt("What would you wish to do? (1/2/3/4/5/6/7)")

        if choice == "1":
            post_tweet(cursor, username)
        elif choice == "2":
            view_timeline(cursor, username)
        elif choice == "3":
            like_tweet(cursor, username)
        elif choice == "4":
            view_likes(cursor)
        elif choice == "5":
            add_comment(cursor, username)
        elif choice == "6":
            follow_user(cursor, username)
        elif choice == "7":
            unfollow_user(cursor, username)


@app.command()
def tweet():
    username = login_user(cursor)
    if username:
        post_tweet(cursor, username)


@app.command()
def timeline():
    username = login_user(cursor)
    if username:
        view_timeline(cursor, username)


@app.command()
def like():
    username = login_user(cursor)
    if username:
        like_tweet(cursor, username)


@app.command()
def likes():
    view_likes(cursor)


@app.command()
def comment():
    username = login_user(cursor)
    if username:
        add_comment(cursor, username)


@app.command()
def follow():
    username = login_user(cursor)
    if username:
        follow_user(cursor, username)


@app.command()
def unfollow():
    username = login_user(cursor)
    if username:
        unfollow_user(cursor, username)


def version_callback(value: bool):
    if value:
        typer.echo(f"Chirrup CLI app: {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def menu():
    # TODO: Add --version flag to this callback
    """
    Start Chirrup CLI and show user menu.
    """
    typer.echo("=== Twitter-like CLI Menu ===")
    while True:
        typer.echo("1. Register")
        typer.echo("2. Login")
        typer.echo("E. Exit")

        choice = typer.prompt("Enter your choice (1/2/E): ")

        if choice == "1":
            register_user(cursor)
        elif choice == "2":
            login()
        elif choice == "E" or choice == "e":
            typer.echo("Exiting the application.")
            raise typer.Exit()
        else:
            typer.echo("Invalid choice.")


if __name__ == "__main__":
    conn = sqlite3.connect(__database_path__, timeout=120)
    cursor = conn.cursor()
    app()
