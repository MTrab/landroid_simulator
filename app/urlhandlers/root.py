"""Root URL handler."""
import web

app = web.auto_application()


class root(app.page):
    """Basic web-root for the service"""

    path = ""

    def GET(self) -> str:
        """HTTP GET handler for the web root."""
        raise web.seeother("sim")


class alt_root(root):
    """Alternative root URI."""

    path = "/"
