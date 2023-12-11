__version__ = "0.1.2"
__app_name__ = "Chirrup"
__database_path__ = "Chirrup.db"

# This is just stashed here in case we need it
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