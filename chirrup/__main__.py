from chirrup import

if __name__ == "__main__":
    db_name = "twitter_like.db"
    cursor = init_cursor(db_name)

    while True:
        main_menu(cursor)

    # Add the following lines to handle your existing CLI commands after the main menu loop:
    app.add_typer(post_tweet, name="post", help="Post a new tweet")
    app.add_typer(view_timeline, name="timeline", help="View your timeline")
    app.add_typer(like_tweet, name="like", help="Like a tweet")
    app.add_typer(view_likes, name="view-likes", help="View likes on a tweet")
    app.add_typer(add_comment, name="comment", help="Add a comment to a tweet")
    app.add_typer(follow_user, name="follow", help="Follow a user")
    app.add_typer(unfollow_user, name="unfollow", help="Unfollow a user")

    app()
