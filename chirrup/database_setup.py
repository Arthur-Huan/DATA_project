import sqlite3
import hashlib
import uuid


# Function to hash the password with salt
def hash_password(password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    return hashed_password, salt


# Function to initialize the database
def initialize_database(database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Create Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT,
        email TEXT,
        profile_image TEXT,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        salt TEXT
    )
    ''')

    # Create Tweets Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
        tweet_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        tweet_content TEXT,
        creation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    ''')

    # Create Followers/Following Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS followers (
        follow_id INTEGER PRIMARY KEY,
        follower_user_id INTEGER,
        following_user_id INTEGER,
        FOREIGN KEY (follower_user_id) REFERENCES users(user_id),
        FOREIGN KEY (following_user_id) REFERENCES users(user_id)
    )
    ''')

    # Create Likes/Retweets Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS likes_retweets (
        like_retweet_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        tweet_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (tweet_id) REFERENCES tweets(tweet_id)
    )
    ''')

    # Create Comments Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        comment_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        tweet_id INTEGER,
        comment_text TEXT,
        comment_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (tweet_id) REFERENCES tweets(tweet_id)
    )
    ''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_database("chirrup.db")
    print("Database setup and initialization completed.")
