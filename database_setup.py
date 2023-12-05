import sqlite3
import hashlib
import uuid


# Function to create a connection to the database
def create_connection():
    return sqlite3.connect("twitter_like.db")


# Function to hash the password with salt
def hash_password(password):
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha256(salt.encode() + password.encode()).hexdigest()
    return hashed_password, salt


# Function to initialize the database
def initialize_database():
    conn = create_connection()
    cursor = conn.cursor()

    # Create User Profiles Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_profiles (
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
        FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
    )
    ''')

    # Create Followers/Following Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS followers_following (
        follow_id INTEGER PRIMARY KEY,
        follower_user_id INTEGER,
        following_user_id INTEGER,
        FOREIGN KEY (follower_user_id) REFERENCES user_profiles(user_id),
        FOREIGN KEY (following_user_id) REFERENCES user_profiles(user_id)
    )
    ''')

    # Create Likes/Retweets Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS likes_retweets (
        like_retweet_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        tweet_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES user_profiles(user_id),
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
        FOREIGN KEY (user_id) REFERENCES user_profiles(user_id),
        FOREIGN KEY (tweet_id) REFERENCES tweets(tweet_id)
    )
    ''')

    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_database()
    print("Database setup and initialization completed.")
