"""Authenticate user logins."""
import hashlib
import sqlite3
import web


class Authenticate:
    """Authentication class."""

    def POST(self):
        """Data from client."""
        input = web.input()

        authdb = sqlite3.connect("users.db")
        pwdhash = hashlib.md5(input.password).hexdigest()
        check = authdb.execute(
            "select * from users where username=? and password=?", (input.username, pwdhash)
        )
        if check:
            session.loggedin = True
            session.username = input.username
            raise web.seeother("/sim")
        else:
            return "Those login details don't work!"
