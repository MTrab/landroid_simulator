"""Authenticate user logins."""
import hashlib
import os
import sqlite3
import web

from app.datasets import Vendor

app = web.auto_application()

# render = web.template.render("static/sim/")
# print(render.index())


class Authenticate(app.page):
    """Authentication class."""

    path = "/authenticate"

    def GET(self):
        """For testing purposes only."""
        web.ctx.session.vendor = Vendor.WORX

    def POST(self):
        """Data from client."""
        indata = web.input()

        authdb = sqlite3.connect("users.db")
        pwdhash = hashlib.md5(indata.password).hexdigest()
        check = authdb.execute(
            "select * from users where username=? and password=?",
            (indata.username, pwdhash),
        )
        if check:
            # web.ctx.session.loggedin = True
            # web.ctx.session.username = indata.username
            raise web.seeother("/sim")
        else:
            return "Those login details don't work!"


class root(app.page):
    """Root simulator page."""

    path = "/"

    def GET(self):
        """Return some test data."""
        return "Test"  # render.index()


class alt_root(root):
    """Used for accessing without / :)"""

    path = ""


class ForgotPassword(app.page):
    """Class for handling forgotten passwords."""

    path = "/lostpass"

    def GET(self):
        """Return some test data."""
        return "Lost password"


class CreateUser:
    """Class for creating users."""

    path = "/create"

    def GET(self):
        """Return some test data."""
        return "Create user"


# app = web.application(urls, locals())
