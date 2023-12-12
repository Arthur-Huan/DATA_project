import typer
import sqlite3
from chirrup import __version__, __app_name__, __database_path__, database_setup
import chirrup.backend as backend  # DO NOT import all as *. There will be overlapping function names.

app = typer.Typer()


def init_cursor():
    database_setup.initialize_database(__database_path__)
    conn = sqlite3.connect(__database_path__, timeout=120)
    cur = conn.cursor()
    return cur


def version_callback(value: bool):
    if value:
        typer.echo(f"{__app_name__} {__version__}")
        raise typer.Exit()


@app.command()
def register():
    cursor = init_cursor()
    backend.register_user(cursor)


@app.command()
def tweet():
    """
    Post a new tweet
    """
    cursor = init_cursor()
    username = backend.login_user(cursor)
    if username:
        backend.post_tweet(cursor, username)
    cursor.connection.commit()
    cursor.connection.close()


@app.callback()
def timeline(
        show_following: bool = typer.Option(False, "--following", "-f",
                                            help="Also show tweets from people you follow.")
):
    """
    View your timeline.
    """
    cursor = init_cursor()
    username = backend.login_user(cursor)
    if username:
        if show_following:
            backend.view_following_timeline(cursor, username)
        else:
            backend.view_timeline(cursor, username)
    cursor.connection.commit()
    cursor.connection.close()


@app.command()
def like():
    """
    Like a tweet with its ID.
    """
    cursor = init_cursor()
    username = backend.login_user(cursor)
    if username:
        backend.like_tweet(cursor, username)
    cursor.connection.commit()
    cursor.connection.close()


@app.command()
def view_likes():
    """
    View the number of likes on a tweet using its ID.
    :return:
    """
    cursor = init_cursor()
    backend.view_likes(cursor)
    cursor.connection.commit()
    cursor.connection.close()


@app.command()
def comment():
    """
    Comment on a tweet.
    """
    cursor = init_cursor()
    username = backend.login_user(cursor)
    if username:
        backend.add_comment(cursor, username)
    cursor.connection.commit()
    cursor.connection.close()


@app.command()
def follow():
    """
    Follow a user.
    """
    cursor = init_cursor()
    username = backend.login_user(cursor)
    if username:
        backend.follow_user(cursor, username)
    cursor.connection.commit()
    cursor.connection.close()


@app.command()
def unfollow():
    """
    Unfollow a user.
    """
    cursor = init_cursor()
    username = backend.login_user(cursor)
    if username:
        backend.unfollow_user(cursor, username)
    cursor.connection.commit()
    cursor.connection.close()


@app.command()
def retweet():
    """
    Retweet a tweet from another user,
    """
    cursor = init_cursor()
    username = backend.login_user(cursor)
    if username:
        backend.retweet_tweet(cursor, username)
    cursor.connection.commit()
    cursor.connection.close()


@app.command()
def login():
    """
    Log in and access actions menu.
    """
    cursor = init_cursor()
    username = backend.login_user(cursor)
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
        typer.echo("8. Retweet a tweet")
        typer.echo("E. Exit")

        while True:
            choice = typer.prompt("What would you wish to do? (1/2/3/4/5/6/7/8/E)")
            if choice == "1":
                backend.post_tweet(cursor, username)
            elif choice == "2":
                backend.view_timeline(cursor, username)
            elif choice == "3":
                backend.like_tweet(cursor, username)
            elif choice == "4":
                backend.view_likes(cursor)
            elif choice == "5":
                backend.add_comment(cursor, username)
            elif choice == "6":
                backend.follow_user(cursor, username)
            elif choice == "7":
                backend.unfollow_user(cursor, username)
            elif choice == "8":
                backend.retweet_tweet(cursor, username)
            elif choice == "E" or choice == "e":
                cursor.connection.commit()
                cursor.connection.close()
                raise typer.Exit()
            else:
                typer.echo("Invalid choice. Please try again.")


@app.command()
def menu():
    """
    Main menu. Returning users can use `login` menu instead.
    Register will allow a user to register.
    Login uses the above function's menu.
    Exist is self-explanatory.
    """
    cursor = init_cursor()
    typer.echo("=== Twitter-like CLI Menu ===")
    while True:
        typer.echo("1. Register")
        typer.echo("2. Login")
        typer.echo("E. Exit")

        choice = typer.prompt("Enter your choice (1/2/E)")

        if choice == "1":
            backend.register_user(cursor)
        elif choice == "2":
            login()
        elif choice == "E" or choice == "e":
            typer.echo("Exiting the application.")
            cursor.connection.commit()
            cursor.connection.close()
            raise typer.Exit()
        else:
            typer.echo("Invalid choice.")


if __name__ == "__main__":
    app()
