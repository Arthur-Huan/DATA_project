from typing import Optional

from chirrup import __version__, __app_name__, __database_path__
from chirrup.backend import *

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def show_help(
        version: Optional[bool] = typer.Option(
            None,
            "--version",
            "-v",
            help="Show name and version of app and exit.",
            callback=_version_callback,
            is_eager=True,
        )
) -> None:
    return


# Initialize database connection
def init_cursor(database_name):
    con = sqlite3.connect(__database_path__, timeout=120)
    cur = con.cursor()
    return cur


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
        app.add_typer(post_tweet, name="post", help="Post a new tweet")
        app.add_typer(view_timeline, name="timeline", help="View your timeline")
        app.add_typer(like_tweet, name="like", help="Like a tweet")
        app.add_typer(view_likes, name="view-likes", help="View likes on a tweet")
        app.add_typer(add_comment, name="comment", help="Add a comment to a tweet")
        app.add_typer(follow_user, name="follow", help="Follow a user")
        app.add_typer(unfollow_user, name="unfollow", help="Unfollow a user")


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


@app.command()
def main_menu(cur):
    typer.echo("=== Twitter-like CLI Menu ===")
    typer.echo("1. Register")
    typer.echo("2. Login")
    typer.echo("3. Exit")

    choice = typer.prompt("Enter your choice (1/2/3): ")

    if choice == "1":
        register_user(cur)
    elif choice == "2":
        login_user(cur)
    elif choice == "3":
        typer.echo("Exiting the application.")
        raise typer.Exit()
    else:
        typer.echo("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    import os
    if not os.path.isfile(__database_path__):
        import chirrup.database_setup
        chirrup.database_setup.initialize_database(__database_path__)
    cursor = init_cursor(__database_path__)
    app()
