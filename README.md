# Chirrup

## About

This is a Python CLI app, done as a mini-project for the DATA 211 course at the University of Calgary. The Chirrup app is a twitter-like app where you can post tweets, like and retweet, and comment to interact with other people. It features a carefully crafted user-friendly menu, as well as individual commands for power users who only want to do specific actions at a time.

Password hashing is used to provide a further layer of protection. Your password is never directly stored.

## Dependencies

To set up the required dependencies for this Python project, use `python -m pip install -r requirements.txt`. Alternatively, if you're using pypoetry, use `poetry update`.

## Usage 

To run Chirrup CLI, execute the following command in your terminal or command prompt:

- If using Ppython: `python -m chirrup menu`
- If using Poetry: `poetry run python -m chirrup menu`

## Database Initialization

As end users should not need to initialize the database, there is no command for it in the CLI. However, you can manually run `database_setup.py` in the `chirrup` sub-directory. Alternatively, use the CLI as usual; a database will be initalized for you.

## CLI Commands:
  comment        Comment on a tweet.
  follow         Follow a user.
  like           Like a tweet with its ID.
  login          Log in and access actions menu.
  menu           Main menu.
  register
  retweet        Retweet a tweet from another user,
  timeline       View your timeline.
  tweet          Post a new tweet
  unfollow       Unfollow a user.
  view-comments  View all comments on a tweet.
  view-likes     View the number of likes on a tweet using its ID.
