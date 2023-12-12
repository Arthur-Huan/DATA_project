from chirrup import __version__, __app_name__, __database_path__, database_setup
from chirrup.backend import *

app = typer.Typer()


def init_cursor():
    database_setup.initialize_database(__database_path__)
    conn = sqlite3.connect(__database_path__, timeout=120)
    cur = conn.cursor()
    return cur


@app.command()
def register():
    cursor = init_cursor()
    register_user(cursor)


@app.command()
def login():
    """
    Login user and prompt for additional commands.
    """
    cursor = init_cursor()
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
        typer.echo("8. Retweet a tweet")
        typer.echo("E. Exit")

        choice = 0
        while True:
            choice = typer.prompt("What would you wish to do? (1/2/3/4/5/6/7/8/E)")
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
            elif choice == "8":
                retweet_tweet(cursor, username)
            elif choice == "E" or choice == "e":
                cursor.connection.commit()
                cursor.connection.close()
                raise typer.Exit()
            else:
                typer.echo("Invalid choice. Please try again.")


@app.command()
def tweet():
    cursor = init_cursor()
    username = login_user(cursor)
    if username:
        post_tweet(cursor, username)
    cursor.connection.commit()
    cursor.connection.close()


@app.command()
def timeline(
        show_following: bool = typer.Option(False, "--following", "-f",
                                            help="Also show tweets from people you follow.")
):
    cursor = init_cursor()
    username = login_user(cursor)
    if username:
        if show_following:
            view_following_timeline(cursor, username)
        else:
            view_timeline(cursor, username)
    cursor.connection.commit()
    cursor.connection.close()


@app.command()
def like():
    cursor = init_cursor()
    username = login_user(cursor)
    if username:
        like_tweet(cursor, username)
    cursor.connection.commit()
    cursor.connection.close()


@app.command()
def view_likes():
    cursor = init_cursor()
    view_likes(cursor)
    cursor.connection.commit()
    cursor.connection.close()


@app.command()
def comment():
    cursor = init_cursor()
    username = login_user(cursor)
    if username:
        add_comment(cursor, username)
    cursor.connection.commit()
    cursor.connection.close()


@app.command()
def follow():
    cursor = init_cursor()
    username = login_user(cursor)
    if username:
        follow_user(cursor, username)
    cursor.connection.commit()
    cursor.connection.close()


@app.command()
def unfollow():
    cursor = init_cursor()
    username = login_user(cursor)
    if username:
        unfollow_user(cursor, username)
    cursor.connection.commit()
    cursor.connection.close()


@app.command()
def retweet():
    cursor = init_cursor()
    username = login_user(cursor)
    if username:
        retweet_tweet(cursor, username)
    cursor.connection.commit()
    cursor.connection.close()


def version_callback(value: bool):
    if value:
        typer.echo(f"{__app_name__} {__version__}")
        raise typer.Exit()


@app.command()
def menu():
    cursor = init_cursor()
    typer.echo("=== Twitter-like CLI Menu ===")
    while True:
        typer.echo("1. Register")
        typer.echo("2. Login")
        typer.echo("E. Exit")

        choice = typer.prompt("Enter your choice (1/2/E)")

        if choice == "1":
            register_user(cursor)
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
