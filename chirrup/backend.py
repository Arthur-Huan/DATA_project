import hashlib
import re
import sqlite3
import uuid

import typer


# Function to hash the password with salt
def hash_password(password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    return hashed_password, salt


def check_username(username, cursor):
    """
    :param username: The username to be checked
    :param cursor: A sqlite3 cursor for the current database
    :return:
        -1      valid username
        1       length not 2~32 chars
        2       if invalid character (should be only numbers, letters, or underscores)
        3       underscore is at start or end of username
        4       username already selected
    """
    if not 2 <= len(username) <= 32:
        return 1
    if not re.compile(r"^[a-zA-Z0-9_]+$").match(username):
        return 2
    if username[0] == "_" or username[-1] == "_":
        return 3
    cursor.execute(f"SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is not None:
        return 4
    # All checks have passed
    return -1


def check_password(password, re_password):
    """
    :param password: The password to be checked
    :param re_password: The re-entered password
    :return:
        -1      Valid password
        1       Passwords don't match
        2       Length not at least 8 characters
        3       Doesn't include a mix of numbers and letters
    """
    if password != re_password:
        return 1
    if not len(password) >= 8:
        return 2
    if not re.compile(r'^(?=.*[a-zA-Z])(?=.*\d).+$').match(password):
        return 3
    # All checks have passed
    return -1


def init_cursor(database_path):
    con = sqlite3.connect(database_path, timeout=120)
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
    # Prompt username, and check validity
    username = typer.prompt("Enter new username")
    username_validity = check_username(username, cur)
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
        # Prompt username again, and check validity
        username = typer.prompt("Enter new username")
        username_validity = check_username(username, cursor)

    # Prompt for a password (and enter password again), and check validity
    password = typer.prompt("Enter new password: ", hide_input=True)
    password_again = typer.prompt("Re-enter password: ", hide_input=True)
    password_validity = check_password(password, password_again)
    while password_validity != -1:
        # Handle different validity cases
        if password_validity == 1:
            typer.echo("Passwords don't match.")
        elif password_validity == 2:
            typer.echo("Password must be at least 8 characters or longer.")
        elif password_validity == 3:
            typer.echo("Password must include a mix of numbers and letters.")
        else:
            typer.echo("Unexpected username formatting issue, please file a bug report.")
        # Prompt for a password (and enter password again), and check validity
        password = typer.prompt("Enter new password: ", hide_input=True)
        password_again = typer.prompt("Re-enter password: ", hide_input=True)
        password_validity = check_password(password, password_again)

    # Store the new user in the database
    # TODO: Store hash instead of the direct password
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    typer.echo("User registered successfully.")

    cur.connection.commit()
    cur.connection.close()


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
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    if cur.fetchone() is not None:
        typer.echo(f"Login successful. Welcome, {username}!")
        return username
    else:
        typer.echo("Invalid username or password. Please try again.")
        return None


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
