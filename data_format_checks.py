import re


def username_check(username, cursor):
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


def password_check(password):
    """
    :param password: The password to be checked
    :return:
        -1      valid password
        1       length not at least 8 characters
        2       Doesn't include a mix of numbers, upper and lowercase letters, and special characters
    """
    if not len(password) >= 8:
        return 1
    if not re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9!@#$%^&*()-_=+{};:,<.>/?`~[\]\\\|])").match(password):
        return 2
    # All checks have passed
    return -1
