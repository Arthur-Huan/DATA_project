import sqlite3

import typer

from data_format_checks import *

app = typer.Typer()


# Initialize database connection
def init_cursor(database_name):
    con = sqlite3.connect(database_name, timeout=120)
    cur = con.cursor()
    return cur


### 3.1 - User Registration & Login ###

# Function to register a new user
def register_user(cur):
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

        # Prompt user for a new username
        username = typer.prompt("Enter new username")
        username_validity = username_check(username, cur)

    # Prompt for a password
    password = typer.prompt("Enter password", hide_input=True)

    # Store the new user in the database
    store_user_in_database(username, password, cur)

    typer.echo("User registered successfully.")


# Function to log in a user
def login_user(cur):
    username = typer.prompt("Enter your username")
    password = typer.prompt("Enter your password", hide_input=True)

    # Check if the provided credentials are valid
    if validate_user_credentials(username, password, cur):
        typer.echo("Login successful. Welcome, {}!".format(username))
        return username
    else:
        typer.echo("Invalid username or password. Please try again.")
        return None


# Function to store a new user in the database
def store_user_in_database(username, password, cur):
    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    cur.connection.commit()


# Function to validate user credentials
def validate_user_credentials(username, password, cur):
    cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cur.fetchone()
    return user is not None


### 3.2 - Posting New Tweets ###

# Function to post a new tweet
def post_tweet(cur, username):
    tweet_text = typer.prompt("Compose your tweet")

    # Store the new tweet in the database
    store_tweet_in_database(username, tweet_text, cur)

    typer.echo("Tweet posted successfully.")


# Function to store a users new tweet in the database
def store_tweet_in_database(username, tweet_text, cur):
    cur.execute("INSERT INTO tweets (username, tweet_text, timestamp) VALUES (?, ?, datetime('now'))",
                (username, tweet_text))
    cur.connection.commit()


### 3.3 - Viewing User's Timeline ###

# Function to view user's timeline
def view_timeline(cur, username):
    # Retrieve and display tweets from the user's timeline (tweets from followed users)
    tweets = get_timeline_for_user(username, cur)

    if tweets:
        for t in tweets:
            typer.echo("{} (@{}): {}".format(t[1], t[0], t[2]))
    else:
        typer.echo("Your timeline is empty.")


# Function to get tweets from users that the given user follows
def get_timeline_for_user(username, cur):
    cur.execute("""
        SELECT t.username, u.username, t.tweet_text, t.timestamp
        FROM tweets t
        JOIN follows f ON t.username = f.followed_username
        JOIN users u ON t.username = u.username
        WHERE f.username = ?
        ORDER BY t.timestamp DESC
    """, (username,))
    return cur.fetchall()


### 3.4 - Liking Tweets ###

def like_tweet(cur, username):
    tweet_id = typer.prompt("Enter the ID of the tweet you want to like")

    # Like the tweet in the database
    like_tweet_in_database(username, tweet_id, cur)

    typer.echo("Tweet liked successfully.")


# Function to like a tweet in the database
def like_tweet_in_database(username, tweet_id, cur):
    cur.execute("INSERT INTO likes (username, tweet_id) VALUES (?, ?)", (username, tweet_id))
    cur.connection.commit()


### 3.5 - Showing the Number of Likes of Tweets ###
''' ** might have to change how this is implemented not sure if the # of likes have to be displayed at all times 
 or if the value just has to be retrievable ** '''


# Function to view the number of likes on a tweet
def view_likes(cur):
    tweet_id = typer.prompt("Enter the ID of the tweet you want to view likes for")

    # Get and display the number of likes for the tweet
    likes_count = get_likes_count(tweet_id, cur)

    if likes_count is not None:
        typer.echo("Tweet {} has {} likes.".format(tweet_id, likes_count))
    else:
        typer.echo("Tweet not found.")

    # Function to get the number of likes for a tweet


def get_likes_count(tweet_id, cur):
    cur.execute("SELECT COUNT(*) FROM likes WHERE tweet_id = ?", (tweet_id,))
    likes_count = cur.fetchone()[0]
    return likes_count


### 3.6 - Comments on Tweets ###

# Function to add a comment to a tweet
def add_comment(cur, username):
    tweet_id = typer.prompt("Enter the ID of the tweet you want to comment on")
    comment_text = typer.prompt("Enter your comment")

    # Store the comment in the database
    store_comment_in_database(username, tweet_id, comment_text, cur)

    typer.echo("Comment added successfully.")


# Function to store a new comment in the database
def store_comment_in_database(username, tweet_id, comment_text, cur):
    cur.execute("INSERT INTO comments (username, tweet_id, comment_text, timestamp) VALUES (?, ?, ?, datetime('now'))",
                (username, tweet_id, comment_text))
    cur.connection.commit()


### 3.7 - Following & Unfollowing Users ###

# Function to follow a user
def follow_user(username, user_to_follow, cur):
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


### 3.9 - Documentation & Help System ###
''' *** current implementation for this portion of the features is a bit barebones will probably need to add more 
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
        if username:
            # If login is successful, show additional commands

            ### 3.8 - User Friendly Menu System ###
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


    app()
