import sqlite3

import typer
from typing import Optional
from chirrup.data_format_checks import *

app = typer.Typer()


# Initialize database connection
def init_cursor(database_name):
    con = sqlite3.connect(database_name, timeout=120)
    cur = con.cursor()
    return cur


# ========================
# 3.1 - User Registration & Login
# ========================

def register_user(cur):
    """
    Registers a user in databse after checking for validity.
    :param cur: SQL cursor
    :return: None
    """
    username = typer.prompt("Enter new username")
    # Check if the username is valid
    username_validity = username_check(username, cur)
    while username_validity != -1:
        # Handle different validity cases
        if username_validity == 1:
            typer.echo("Length of username should be between 2 to 32 characters.")
        elif username_validity == 2:
            typer.echo("Username contains invalid characters. Only letters, numbers, and underscores are allowed.")
        elif username_validity == 3:
            typer.echo("Underscores should not be at the start or end of a username.")
        elif username_validity == 4:
            typer.echo("Username already in use.")
        else:
            typer.echo("Unexpected username formatting issue, please file a bug report.")
        # Prompt username again
        username = typer.prompt("Enter new username")
        username_validity = username_check(username, cur)

    # TODO: Confirmation for password
    # Prompt for a password
    password = typer.prompt("Enter password", hide_input=True)

    # Store the new user in the database
    # TODO: Store hash instead of the direct password
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    typer.echo("User registered successfully.")


def login_user(cur):
    """
    Log in a user, checking username and password in the database.
    :param cur: SQL cursor
    :return:
            username if successful login
            None otherwise
    """
    username = typer.prompt("Enter your username")
    password = typer.prompt("Enter your password", hide_input=True)
    # TODO: Use hashing instead of password
    # Check if the provided credentials are valid
    if validate_user_credentials(username, password, cur):
        typer.echo(f"Login successful. Welcome, {username}!")
        return username
    else:
        typer.echo("Invalid username or password. Please try again.")
        return None


def validate_user_credentials(username, password, cur):
    """
    Validate user credentials
    :param username: Inputted username to check
    :param password: Inputted password to check
    :param cur: SQL cursor
    :return:
    """
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    return user is not None


# ========================
# 3.2 - Posting New Tweets
# ========================

def post_tweet(cur, username):
    """
    'Posts' a tweet by storing it in the tweet database. Assumes user is already logged in.
    :param cur: SQL cursor
    :param username: The username of the person tweeting.
    :return: None
    """
    tweet_text = typer.prompt("Compose your tweet")
    cur.execute("INSERT INTO tweets (username, tweet_text, timestamp) VALUES (?, ?, datetime('now'))",
                (username, tweet_text))
    typer.echo("Tweet posted successfully.")


# ========================
# 3.3 - Viewing User's Timeline
# ========================


def view_timeline(cur, username):
    """
    Prints the user's timeline. Assumes user is already logged in.
    :param cur: SQL cursor
    :param username: Username of user
    :return: None
    """
    # Retrieve and display tweets from the user's timeline (tweets from followed users)
    cur.execute("""
        SELECT t.username, u.username, t.tweet_text, t.timestamp
        FROM tweets t
        JOIN follows f ON t.username = f.followed_username
        JOIN users u ON t.username = u.username
        WHERE f.username = ?
        ORDER BY t.timestamp DESC
    """, (username,))

    tweets = cur.fetchall()
    if tweets:
        for t in tweets:
            typer.echo("{} (@{}): {}".format(t[1], t[0], t[2]))
    else:
        typer.echo("Your timeline is empty.")


# ========================
# 3.4 - Liking Tweets
# ========================

# TODO: Behavior is seemingly wrong, it should be either insert into for the first like, or add a value to likes,
# or, just initialize with 0 and add 1 to the value
def like_tweet(cur, username):
    tweet_id = typer.prompt("Enter the ID of the tweet you want to like")
    cur.execute("INSERT INTO likes_retweets (username, tweet_id) VALUES (?, ?)", (username, tweet_id))
    typer.echo("Tweet liked successfully.")


# ========================
# 3.5 - Showing the Number of Likes of Tweets
# ========================


''' TODO: might have to change how this is implemented not sure if the # of likes have to be displayed at all times 
or if the value just has to be retrievable'''


# Function to view the number of likes on a tweet
def view_likes(cur):
    tweet_id = typer.prompt("Enter the ID of the tweet you want to view likes for")
    cur.execute("SELECT COUNT(*) FROM likes_retweets WHERE tweet_id = ?", (tweet_id,))
    likes_count = cur.fetchone()[0]
    if likes_count is not None:
        typer.echo("Tweet {} has {} likes.".format(tweet_id, likes_count))
    else:
        typer.echo("Tweet not found.")


# ========================
# 3.6 - Comments on Tweets
# ========================


# Function to add a comment to a tweet
def add_comment(cur, username):
    tweet_id = typer.prompt("Enter the ID of the tweet you want to comment on")
    comment_text = typer.prompt("Enter your comment")
    # Store the comment in the database
    cur.execute("INSERT INTO comments (username, tweet_id, comment_text, timestamp) VALUES (?, ?, ?, datetime('now'))",
                (username, tweet_id, comment_text))
    typer.echo("Comment added successfully.")


# ========================
# 3.7 - Following & Unfollowing Users
# ========================


def follow_user(username, user_to_follow, cur):
    """
    Function to follow a user
    """
    # Check if the user exists
    cur.execute("SELECT 1 FROM users WHERE username = ?", (user_to_follow,))
    user_exists = cur.fetchone()

    if user_exists:
        # Check if the user is not already being followed
        cur.execute("SELECT 1 FROM follows WHERE username = ? AND followed_username = ?", (username, user_to_follow))
        already_following = cur.fetchone()

        if not already_following:
            # Follow the user in the database
            cur.execute("INSERT INTO follows (username, followed_username) VALUES (?, ?)", (username, user_to_follow))
            cur.connection.commit()
            typer.echo("You are now following {}.".format(user_to_follow))
        else:
            typer.echo("You are already following {}.".format(user_to_follow))
    else:
        typer.echo("User {} does not exist.".format(user_to_follow))


# Function to unfollow a user
def unfollow_user(username, user_to_unfollow, cur):
    # Check if the user is being followed
    cur.execute("SELECT 1 FROM follows WHERE username = ? AND followed_username = ?", (username, user_to_unfollow))
    is_following = cur.fetchone()

    if is_following:
        # Unfollow the user in the database
        cur.execute("DELETE FROM follows WHERE username = ? AND followed_username = ?", (username, user_to_unfollow))
        cur.connection.commit()
        typer.echo("You have unfollowed {}.".format(user_to_unfollow))
    else:
        typer.echo("You are not following {}.".format(user_to_unfollow))


# ========================
# 3.9 - Documentation & Help System
# ========================


''' TODO: current implementation for this portion of the features is a bit barebones will probably need to add more 
to make it more specific for different use cases '''


@app.callback()
def show_help():
    """
    CLI application for a Twitter-like service.

    This application provides the following functionalities:

    3.1 User Registration and Login:
        - Users can create new accounts with unique usernames.
        - Users can securely log in using their credentials.

    3.2 Posting New Tweets:
        - Users can post new tweets.
        - Users enter the text of their tweets, which is added to the database with a timestamp.

    3.3 Viewing User’s Timeline:
        - Users can view their timeline, displaying tweets from the users they follow.
        - Timeline shows the most recent tweets first.

    3.4 Liking Tweets:
        - Users can like tweets to express their interest.

    3.5 Showing the Number of Likes of Tweets:
        - The application displays the number of likes each tweet has received.

    3.6 Comments on Tweets:
        - Users can add comments to tweets.
        - Users can view comments on tweets and add their own comments for discussions.

    3.7 Following and Unfollowing Users:
        - Users can follow or unfollow other users.
        - This feature allows users to build their network and customize their timeline.
    """
    pass


if __name__ == "__main__":
    db_name = "twitter_like.db"
    cursor = init_cursor(db_name)


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


def main_menu(cur):
    typer.echo("=== Twitter-like CLI Menu ===")
    typer.echo("1. Register")
    typer.echo("2. Login")
    typer.echo("3. Exit")

    choice = typer.prompt("Enter your choice (1/2/3): ")

    if choice == "1":
        register_user(cur)
    elif choice == "2":
        username = login_user(cur)
        if username:
            # If login is successful, show additional commands
            typer.echo("Welcome, {}!".format(username))
            app.add_typer(post_tweet, name="post", help="Post a new tweet")
            # ... (add more commands)
    elif choice == "3":
        typer.echo("Exiting the application.")
        raise typer.Exit()
    else:
        typer.echo("Invalid choice. Please enter 1, 2, or 3.")
